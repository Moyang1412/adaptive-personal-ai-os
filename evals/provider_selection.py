#!/usr/bin/env python3
"""Small, side-effect-free provider assessment and routing reference.

This module does not store records, search history, migrate data, or implement a
memory engine. It evaluates host-reported provider descriptors and returns a
conservative plan that a Skill or host adapter can present to a user.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import FrozenSet, Iterable


CAPABILITIES: FrozenSet[str] = frozenset(
    {
        "save",
        "read",
        "correct",
        "delete",
        "scope",
        "cross_session",
        "cross_agent",
        "concurrent_write_guard",
        "import_export",
    }
)
ACTIVE_MAINTENANCE = frozenset({"active", "maintained"})
UNKNOWN_METADATA = frozenset({"", "unknown", "unverified", "not verified", "n/a"})
WRITE_OPERATIONS = frozenset(
    {"save", "correct", "delete", "import", "export"}
)


def _require_boolean_fields(value: object, *names: str) -> None:
    # Type annotations alone do not prevent a truthy JSON/config string such as
    # "false" from being treated as verification or authorization.
    for name in names:
        if type(getattr(value, name)) is not bool:
            raise ValueError(f"{name} must be a boolean")


@dataclass(frozen=True)
class ProviderEvidence:
    """Separate documentation claims from observations in the current host."""

    documented: bool = False
    installed: bool = False
    enabled: bool = False
    callable: bool = False
    isolated_test: bool = False

    def __post_init__(self) -> None:
        _require_boolean_fields(self, 'documented', 'installed', 'enabled', 'callable', 'isolated_test')


@dataclass(frozen=True)
class ProviderDescriptor:
    """Host-reported metadata for one potential memory provider."""

    id: str
    name: str
    version: str
    kind: str
    location: str
    local: bool
    network_required: bool
    capabilities: FrozenSet[str]
    storage_location: str
    license: str
    maintenance_status: str
    interface: str
    source_of_truth: str
    evidence: ProviderEvidence = field(default_factory=ProviderEvidence)
    verified_capabilities: FrozenSet[str] = frozenset()
    unverified_capabilities: FrozenSet[str] = frozenset()

    def __post_init__(self) -> None:
        _require_boolean_fields(self, 'local', 'network_required')
        if not isinstance(self.evidence, ProviderEvidence):
            raise ValueError('evidence must be a ProviderEvidence value')
        # Snapshot caller-owned sets: later mutation must not silently change
        # which capabilities this validated descriptor claims or has verified.
        for name in ('capabilities', 'verified_capabilities', 'unverified_capabilities'):
            object.__setattr__(self, name, frozenset(getattr(self, name)))
        if not self.id.strip():
            raise ValueError("provider id must not be empty")
        if not self.name.strip():
            raise ValueError("provider name must not be empty")
        if not self.version.strip():
            raise ValueError("provider version must not be empty")
        if not self.kind.strip():
            raise ValueError("provider kind must not be empty")
        if not self.location.strip():
            raise ValueError("provider location must not be empty")
        if not self.storage_location.strip():
            raise ValueError("storage location must not be empty")
        if not self.source_of_truth.strip():
            raise ValueError("source of truth must not be empty")
        unknown = set(self.capabilities) - CAPABILITIES
        if unknown:
            raise ValueError(f"unknown capabilities: {sorted(unknown)}")
        for label, values in (
            ("verified", self.verified_capabilities),
            ("unverified", self.unverified_capabilities),
        ):
            unknown = set(values) - set(self.capabilities)
            if unknown:
                raise ValueError(f"unknown {label} capabilities: {sorted(unknown)}")
        overlap = set(self.verified_capabilities) & set(self.unverified_capabilities)
        if overlap:
            raise ValueError(f"capabilities cannot be both verified and unverified: {sorted(overlap)}")


@dataclass(frozen=True)
class MemoryRequirements:
    """The minimum scope requested for this first long-term-memory decision."""

    persistent: bool
    required_capabilities: FrozenSet[str]
    cross_agent: bool
    explicit_gap: bool
    user_consent: str
    private_profile_authorized: bool = False
    private_profile_conflict_control: bool = False

    def __post_init__(self) -> None:
        _require_boolean_fields(self, 'persistent', 'cross_agent', 'explicit_gap',
                                'private_profile_authorized', 'private_profile_conflict_control')
        object.__setattr__(self, 'required_capabilities', frozenset(self.required_capabilities))
        unknown = set(self.required_capabilities) - CAPABILITIES
        if unknown:
            raise ValueError(f"unknown required capabilities: {sorted(unknown)}")
        if self.user_consent not in {"off", "confirm", "authorized"}:
            raise ValueError("user_consent must be off, confirm or authorized")
        if self.cross_agent and "cross_agent" not in self.required_capabilities:
            raise ValueError("cross_agent requests must require cross_agent capability")


@dataclass(frozen=True)
class ProviderAssessment:
    provider_id: str
    ready: bool
    eligible: bool
    verified_capabilities: FrozenSet[str]
    unverified_capabilities: FrozenSet[str]
    unsupported_capabilities: FrozenSet[str]
    reasons: tuple[str, ...]


@dataclass(frozen=True)
class RecommendationPlan:
    option: str
    provider_id: str | None
    reasons: tuple[str, ...]
    requires_explicit_scope: bool = False


class ProviderOperation(str, Enum):
    SAVE = "save"
    READ = "read"
    CORRECT = "correct"
    DELETE = "delete"
    IMPORT = "import"
    EXPORT = "export"


@dataclass(frozen=True)
class RouteRequest:
    operation: ProviderOperation
    scope: str
    user_consent: str
    authorized_scopes: FrozenSet[str]
    network_allowed: bool
    active_provider_id: str | None = None
    relevant: bool = True
    cross_agent: bool = False
    sharing_authorized: bool = False
    single_writer: bool = False

    def __post_init__(self) -> None:
        _require_boolean_fields(self, 'network_allowed', 'relevant', 'cross_agent', 'sharing_authorized', 'single_writer')
        if isinstance(self.authorized_scopes, (str, bytes)):
            raise ValueError('authorized_scopes must be a collection of scopes, not text')
        object.__setattr__(self, 'authorized_scopes', frozenset(self.authorized_scopes))


@dataclass(frozen=True)
class RouteResult:
    status: str
    provider_id: str | None
    reason: str


class SourceConflictError(ValueError):
    """Raised when more than one provider would write the same source."""


def evaluate_trigger(*, first_long_term_need: bool, already_evaluated: bool) -> bool:
    """Evaluate once when a user first asks for continuity across sessions."""

    return first_long_term_need and not already_evaluated


def _ensure_single_source(providers: Iterable[ProviderDescriptor]) -> None:
    sources: dict[str, str] = {}
    identities: set[str] = set()
    for provider in providers:
        if provider.id in identities:
            raise SourceConflictError(f"provider id {provider.id!r} is ambiguous")
        identities.add(provider.id)
        previous = sources.get(provider.source_of_truth)
        if previous and previous != provider.id:
            raise SourceConflictError(
                f"source {provider.source_of_truth!r} has multiple writers: "
                f"{previous} and {provider.id}"
            )
        sources[provider.source_of_truth] = provider.id


def assess_provider(
    provider: ProviderDescriptor, requirements: MemoryRequirements
) -> ProviderAssessment:
    """Return conservative readiness without touching the provider's data."""

    required = set(requirements.required_capabilities)
    if requirements.cross_agent:
        required.add("concurrent_write_guard")
    ready = (
        provider.evidence.installed
        and provider.evidence.enabled
        and provider.evidence.callable
    )
    available = required.intersection(provider.capabilities)
    unsupported = required - set(provider.capabilities)
    declared_verified = set(provider.verified_capabilities)
    verified = (
        available.intersection(declared_verified)
        if ready and provider.evidence.isolated_test
        else set()
    )
    unverified = available - verified
    reasons: list[str] = []

    if not provider.evidence.documented:
        reasons.append("官方能力说明未找到")
    if not provider.evidence.installed:
        reasons.append("当前环境未安装")
    if not provider.evidence.enabled:
        reasons.append("当前配置未启用")
    if not provider.evidence.callable:
        reasons.append("当前会话不可调用")
    if not provider.evidence.isolated_test:
        reasons.append("隔离测试尚未验证")
    if unsupported:
        reasons.append(f"缺少能力: {', '.join(sorted(unsupported))}")
    if provider.license.strip().lower() in UNKNOWN_METADATA:
        reasons.append("许可证未知")
    if provider.maintenance_status not in ACTIVE_MAINTENANCE:
        reasons.append("维护状态不明确或已停止")
    if provider.interface.strip().lower() in UNKNOWN_METADATA:
        reasons.append("接口标识未知")
    if unverified:
        reasons.append(f"能力未通过隔离验证: {', '.join(sorted(unverified))}")

    eligible = bool(
        ready
        and provider.evidence.isolated_test
        and provider.evidence.documented
        and not unsupported
        and required.issubset(verified)
        and provider.license.strip().lower() not in UNKNOWN_METADATA
        and provider.maintenance_status in ACTIVE_MAINTENANCE
        and provider.interface.strip().lower() not in UNKNOWN_METADATA
    )
    if eligible:
        reasons.append("安装、启用、调用和隔离能力均已验证")
    else:
        reasons.append("不能把该 provider 当作已验证可用方案")

    return ProviderAssessment(
        provider_id=provider.id,
        ready=ready,
        eligible=eligible,
        verified_capabilities=frozenset(verified),
        unverified_capabilities=frozenset(unverified),
        unsupported_capabilities=frozenset(unsupported),
        reasons=tuple(reasons),
    )


def recommend_plan(
    requirements: MemoryRequirements,
    *,
    native_available: bool,
    native_capabilities: FrozenSet[str],
    providers: Iterable[ProviderDescriptor],
) -> RecommendationPlan:
    """Select A/B/C/D without inventing an installed or tested engine."""

    if type(native_available) is not bool:
        raise ValueError('native_available must be a boolean')

    if requirements.user_consent == "off":
        return RecommendationPlan("D", None, ("用户选择暂不使用长期记忆",))
    if not requirements.persistent:
        return RecommendationPlan("D", None, ("当前请求不需要跨会话保存",))

    native_covers = requirements.required_capabilities.issubset(native_capabilities)
    if native_available and native_covers and not requirements.cross_agent:
        return RecommendationPlan(
            "A",
            None,
            ("当前 Agent 的原生记忆已经覆盖本次需求",),
        )

    provider_list = tuple(providers)
    _ensure_single_source(provider_list)

    assessments = [assess_provider(provider, requirements) for provider in provider_list]
    eligible = [
        assessment
        for provider, assessment in zip(provider_list, assessments)
        if assessment.eligible and provider.kind in {"installed-tool", "external-engine"}
    ]
    if requirements.explicit_gap and eligible:
        selected = sorted(eligible, key=lambda item: item.provider_id)[0]
        return RecommendationPlan(
            "C",
            selected.provider_id,
            ("发现明确能力缺口，且已安装并通过隔离验证的 provider 可以补足",),
            requires_explicit_scope=True,
        )

    if (
        requirements.cross_agent
        and native_available
        and requirements.private_profile_authorized
        and requirements.private_profile_conflict_control
    ):
        return RecommendationPlan(
            "B",
            None,
            ("跨 Agent 共享是明确需求，使用精选私人档案并保留原生记忆",),
            requires_explicit_scope=True,
        )

    reasons = ["没有满足当前范围、许可证、维护和隔离验证要求的额外 provider"]
    if assessments:
        reasons.append("已安装或文档声称支持不等于当前会话可调用")
        if any(assessment.unverified_capabilities for assessment in assessments):
            reasons.append("部分能力尚未验证")
    if requirements.explicit_gap:
        reasons.append("先暂不使用额外引擎，等待用户选择并完成验证")
    return RecommendationPlan("D", None, tuple(reasons))


def route_operation(request: RouteRequest, provider: ProviderDescriptor) -> RouteResult:
    """Authorize one operation; no success is returned for a blocked write."""

    if not isinstance(request.operation, ProviderOperation):
        return RouteResult("blocked", provider.id, "未知的 provider 操作")
    if request.user_consent != "authorized":
        return RouteResult("blocked", provider.id, "本次操作尚未获得明确授权")
    if request.active_provider_id != provider.id:
        return RouteResult("blocked", provider.id, "provider 不是当前选中的写入来源")
    if not request.relevant:
        return RouteResult("blocked", provider.id, "当前请求与长期记忆无关")
    if not request.scope.strip() or request.scope not in request.authorized_scopes:
        return RouteResult("blocked", provider.id, "当前范围未获授权")
    if request.cross_agent:
        if not request.sharing_authorized:
            return RouteResult("blocked", provider.id, "跨 Agent 共享尚未授权")
        if "cross_agent" not in provider.verified_capabilities:
            return RouteResult("blocked", provider.id, "provider 的跨 Agent 能力尚未验证")
        if (
            request.operation.value in WRITE_OPERATIONS
            and "concurrent_write_guard" not in provider.verified_capabilities
            and not request.single_writer
        ):
            return RouteResult("blocked", provider.id, "共享写入没有版本/锁保护或单写入者")
    capability = (
        "import_export"
        if request.operation in {ProviderOperation.IMPORT, ProviderOperation.EXPORT}
        else request.operation.value
    )
    if not provider.evidence.isolated_test:
        return RouteResult("blocked", provider.id, "provider 尚未通过隔离测试")
    if "scope" not in provider.verified_capabilities:
        return RouteResult("blocked", provider.id, "provider 的范围控制尚未验证")
    if capability not in provider.verified_capabilities:
        return RouteResult("blocked", provider.id, "provider 的该操作尚未验证")
    if not (
        provider.evidence.installed
        and provider.evidence.enabled
        and provider.evidence.callable
    ):
        return RouteResult("blocked", provider.id, "provider 当前不可调用")
    if (
        provider.license.strip().lower() in UNKNOWN_METADATA
        or provider.maintenance_status not in ACTIVE_MAINTENANCE
        or provider.interface.strip().lower() in UNKNOWN_METADATA
    ):
        return RouteResult("blocked", provider.id, "provider 的许可证、维护状态或接口未确认")
    if provider.network_required and not request.network_allowed:
        return RouteResult("blocked", provider.id, "provider 需要联网但本次未授权联网")

    if request.operation.value in WRITE_OPERATIONS and not provider.evidence.isolated_test:
        return RouteResult("blocked", provider.id, "写入 provider 尚未通过隔离测试")
    return RouteResult("provider", provider.id, "已按授权范围路由给选中的 provider")
