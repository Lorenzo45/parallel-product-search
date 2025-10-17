import os
import argparse

from parallel import Parallel
from pydantic import BaseModel, Field
from typing import Literal

class ProductOutput(BaseModel):
    title: str = Field(
        description="The official name of the product"
    )
    price: float = Field(
        description="The price of the product to buy it outright (NOT monthly installment price)"
    )
    currency: str = Field(
        description="The currency of the product's price (e.g. USD, EUR, GBP)"
    )
    url: str = Field(
        description="The URL where the product details are available"
    )

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", required=True, help="The product to search for")
    args = parser.parse_args()

    client = Parallel(api_key=os.getenv("PARALLEL_API_KEY"))

    task_run = client.task_run.create(
        input=args.query,
        task_spec={
          "output_schema":{
            "type":"json",
            "json_schema":ProductOutput.model_json_schema()
          }
        },
        processor="base"
    )
    print(f"Running Parallel task with run ID: {task_run.run_id}")

    run_result = client.task_run.result(task_run.run_id, api_timeout=3600)
    print("Run Result:", run_result.output)
    print("-----")
    print("Output:", run_result.output.content)

if __name__ == "__main__":
    main()