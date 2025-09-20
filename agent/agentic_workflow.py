from utils.model_loader import ModelLoader
from prompt_library.prompt import SYSTEM_PROMPT
from langgraph.graph import StateGraph, MessageState, END, START
from langgraph.prebuilt import ToolNode, tools_condition


# from tools.weather_info_tool import WeatherInfoTool
# from tools.expense_calculator_tool import CalculatorTool
# from tools.place_search_tool import PlaceSearchTool
# from tools.currency_conversion_tool import CurrencyConvertorTool




class GraphBuilder():
    def __init__(self):
        self.tools=[
            # WeatherInfoTool(),
        ]   
        self.system_prompt=SYSTEM_PROMPT
        

    def agent_function(self, state:MessageState):
        """Main agent function to process user input and generate responses.
        """
        user_question=state["messages"]
        input_question=[self.system_prompt]+user_question
        response=self.llm_with_tools.invoke_tool(input_question)
        return{"messages":[response]}
    

    def build_graph(self):
        graph_builder = StateGraph(MessageState)
        graph_builder.add_node("agent",self.agent_function)
        graph_builder.add_node("tools",ToolNode(tools=self.tools))
        graph_builder.add_edge(START,"agent")
        graph_builder.add_conditional_edge("agent",tools_condition)
        graph_builder.add_edge("tools","agent")
        graph_builder.add_edge("agent",END)

        self.graph =graph_builder.compile()
        
    

    def __call__(self):
        return self.build_graph()
