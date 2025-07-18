from src.core_module.strategy_group.groups.sgroup_mcp_json_reporter import MCPJsonReporter


class StrategyFactory:

    @classmethod
    def get_strategy(cls, strategy_name, **kwargs):
        
        if strategy_name == "mcp_json_reporter":
            return MCPJsonReporter()