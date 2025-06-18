from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

from crewai_tools import SerperDevTool
from src.mytripplanner.tools.custom_tool import WeatherForecastTool

@CrewBase
class Mytripplanner():
	"""Mytripplanner crew"""
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'
	@agent
	def destination_data_researcher_agent(self)->Agent:
		return Agent(
			config=self.agents_config['destination_data_researcher_agent'],verbose=True,tools=[SerperDevTool(), WeatherForecastTool()]
		)
	@agent
	def local_expert_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['local_expert_agent'],verbose=True,tools=[SerperDevTool()]
		)
	@agent
	def itinerary_planner_agent(self)-> Agent:
		return Agent(
			config=self.agents_config['itinerary_planner_agent'],verbose=True
		)
	@agent
	def budget_advisor_agent(self)->Agent:
		return Agent(
			config=self.agents_config['budget_advisor_agent'],Verbose=True
		)
	@agent
	def travel_summary_agent(self)-> Agent:
		return Agent(
			config=self.agents_config['travel_summary_agent'],verbose=True
		)
	@task
	def destination_research_task(self)->Task:
		return Task(
			config=self.tasks_config['destination_research_task']
		)
	@task
	def local_insight_task(self)->Task:
		return Task(
			config=self.tasks_config['local_insight_task']
		)
	@task
	def itinerary_task(self)-> Task:
		return Task(
			config=self.tasks_config['itinerary_task']
		)
	@task
	def budget_estimate_task(self)->Task:
		return Task(
			config=self.tasks_config['budget_estimate_task']
		)
	@task 
	def travel_summary_task(self):
		return Task(
			config=self.tasks_config['travel_summary_task']
		)
	@crew
	def crew(self) -> Crew:
		return Crew(
			agents=self.agents,
			tasks=self.tasks,
			process=Process.sequential,
			verbose=True,
		)

	