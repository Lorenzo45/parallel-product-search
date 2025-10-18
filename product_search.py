import os
import argparse
import json

from parallel import Parallel
from pydantic import BaseModel, Field
from typing import Literal

class ProductOutput(BaseModel):
    title: str = Field(
        description="The official name of the product"
    )
    price: float = Field(
        description="The most up-to-date price of the product to buy it outright (NOT monthly installment price)"
    )
    currency: str = Field(
        description="The currency of the product's price (e.g. USD, EUR, GBP)"
    )
    url: str = Field(
        description="The best URL where someone can find product details and purchase the product"
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
        processor="core"
    )
    print(f"Running Parallel task with run ID: {task_run.run_id}")

    run_result = client.task_run.result(task_run.run_id, api_timeout=3600)

    json_output = {"query": args.query, "matched_product": run_result.output.content}
    print(json.dumps(json_output, indent=2))

if __name__ == "__main__":
    main()