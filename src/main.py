import concurrent.futures
import logging
import subprocess
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_script(script_name):
    script_path = f"/app/src/{script_name}"
    logger.info(f"Running {script_path}...")
    start_time = time.time()
    result = subprocess.run(['python', script_path], capture_output=True, text=True)
    end_time = time.time()
    logger.info(f"Finished {script_path} in {end_time - start_time} seconds with return code {result.returncode}")
    if result.returncode != 0:
        logger.error(f"Error in {script_path}: {result.stderr}")
    return result

def main():
    scripts = ['Contacts.py', 'Deals.py', 'Companies.py']
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {executor.submit(run_script, script): script for script in scripts}
        for future in concurrent.futures.as_completed(futures):
            script = futures[future]
            try:
                future.result()
            except Exception as exc:
                logger.error(f"{script} generated an exception: {exc}")

if __name__ == '__main__':
    main()


# import concurrent.futures
# import logging
# import subprocess
# import time


# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)


# def run_script(script_name):
#     logger.info(f"Running {script_name}...")
#     start_time = time.time()
#     result = subprocess.run(['python', script_name], capture_output=True, text=True)
#     end_time = time.time()
#     logger.info(f"Finished {script_name} in {end_time - start_time} seconds with return code {result.returncode}")
#     if result.returncode != 0:
#         logger.error(f"Error in {script_name}: {result.stderr}")
#     return result


# def main():
#     scripts = ['Contacts.py', 'Deals.py', 'Companies.py']
#     with concurrent.futures.ThreadPoolExecutor() as executor:
#         futures = {executor.submit(run_script, script): script for script in scripts}
#         for future in concurrent.futures.as_completed(futures):
#             script = futures[future]
#             try:
#                 future.result()
#             except Exception as exc:
#                 logger.error(f"{script} generated an exception: {exc}")

# if __name__ == '__main__':
#     main()

