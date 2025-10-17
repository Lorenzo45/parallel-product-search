import os

from parallel import Parallel
from pydantic import BaseModel, Field
from typing import Literal

class CompanyOutput(BaseModel):
    founding_date: str = Field(
        description="The official founding date of the company in the format MM-YYYY"
    )
    employee_count: Literal[
        "1-10 employees",
        "11-50 employees",
        "51-200 employees",
        "201-500 employees",
        "501-1000 employees",
        "1001-5000 employees",
        "5001-10000 employees",
        "10001+ employees"
    ] = Field(
        description="The range of employees working at the company. Choose the most accurate range possible and make sure to validate across multiple sources."
    )
    funding_sources: str = Field(
        description="A detailed description, containing 1-4 sentences, of the company's funding sources, including their estimated value."
    )

def main():
    client = Parallel(api_key=os.getenv("PARALLEL_API_KEY"))

    task_run = client.task_run.create(
        input="United Nations",
        task_spec={
          "output_schema":{
            "type":"json",
            "json_schema":CompanyOutput.model_json_schema()
          }
        },
        processor="core"
    )
    print(f"Run ID: {task_run.run_id}")

    run_result = client.task_run.result(task_run.run_id, api_timeout=3600)
    print(run_result.output)

if __name__ == "__main__":
    main()