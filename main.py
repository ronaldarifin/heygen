import asyncio
from client.statusclient import StatusClient

async def get_task_status(task_id: str):
    async with StatusClient() as client:
        # Make multiple status checks
        tasks = []
        for i in range(3):  # Example: make 3 concurrent status checks
            task_id_with_suffix = f"{task_id}_{i}"
            print(f"Sending request for task {task_id_with_suffix}...")
            tasks.append(client.wait_for_completion(task_id_with_suffix))
        
        # Wait for all tasks to complete
        results = await asyncio.gather(*tasks)
        return results

async def main():
    results = await get_task_status("test_taskk")
    print(f"Task results: {results}")

if __name__ == "__main__":
    asyncio.run(main())
