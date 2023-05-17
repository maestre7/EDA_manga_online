#
#   It runs in multithreaded mode when the number of input functions is greater than the number
#   of available CPU cores to avoid thread overuse. If more threads are running than the CPU
#   can handle, this can result in lower performance due to the cost of switching between
#   threads and competing for CPU resources.
#
#   Instead, when using multithreaded mode, each process will run on a separate CPU core,
#   which can increase performance on systems with multiple available CPU cores and prevent
#   thread overload.
#
#   The function first determines the maximum number of threads to use based on the max_threads
#   argument or the number of CPU cores if not specified. Then, it creates a ThreadPoolExecutor
#   with the specified number of threads.
#
#   Next, it executes the functions in parallel using executor.submit() method. If the function
#   is a tuple, it extracts the function and arguments and passes them to executor.submit().
#
#   After executing all the functions, the function waits for them to complete using the as_completed()
#   function. It then processes the results and stores them in a list. If an exception is raised
#   during execution, it is caught and stored in the list of results.
#
#   Finally, the function returns the list of results obtained by executing the functions in parallel.
#

from os import cpu_count
from typing import List, Tuple, Union, Any
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed, Executor, Future


def execute_concurrency(functions: List[Union[callable, Tuple[callable, tuple]]],
                        concurrency_type: str = 'threads',
                        max_concurrency: int = None
                        ) -> List[Any]:
    """
    Executes the given functions in parallel using the specified concurrency type.

    Args:
        functions (List[Union[callable, Tuple[callable, tuple]]]): A list of functions to be executed.
        concurrency_type (str, optional): The type of concurrency to use: 'threads' or 'processes'. Defaults to 'threads'.
        max_concurrency (int, optional): The maximum number of threads or processes to use. Defaults to None.

    Returns:
        List[Any]: A list of results obtained by executing the functions in parallel.
    """

    if concurrency_type == 'threads':
        futures = execute_in_threads(functions, max_threads=max_concurrency)
    elif concurrency_type == 'processes':
        futures = execute_in_processes(functions, max_processes=max_concurrency)
    else:
        raise ValueError(f"Invalid concurrency type: {concurrency_type}. Supported types are 'threads' and 'processes'.")

    # procesar los resultados
    results = []
    for future in as_completed(futures):
        try:
            result = future.result()
        except Exception as err:
            result = err
        results.append(result)

    return results

def execute_in_threads(functions: List[Union[callable, Tuple[callable, tuple]]],
                       max_threads: int = None
                       ) -> List[Any]:
    """The execute_in_threads function takes a list of functions or tuples of function and arguments,
    and an optional maximum number of threads to use. It returns a list of results obtained by 
    executing the functions in parallel.

    Arguments:

    functions (List[Union[callable, Tuple[callable, tuple]]]): A list of functions to be executed in
    parallel or tuples of function and arguments.
    max_threads (int, optional): The maximum number of threads to use. If not specified, 
    the number of CPU cores is used.

    Returns:

    List[Any]: A list of results obtained by executing the functions in parallel
    """

    # determine the maximum number of threads
    if max_threads is None:
        max_threads = cpu_count()

    # create an executor pool
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        # execute functions in parallel
        return execute_with_executor(executor, functions)


def execute_in_processes(functions: List[Union[callable, Tuple[callable, tuple]]],
                        max_processes: int = None
                        ) -> List[Any]:
    """
    Executes the given functions in parallel using multiple processes.

    Args:
        functions (List[Union[callable, Tuple[callable, tuple]]]): A list of functions to be executed.
        max_processes (int, optional): The maximum number of processes to use. Defaults to None.

    Returns:
        List[Any]: A list of results obtained by executing the functions in parallel.
    """

    if max_processes is None:
        max_processes = cpu_count()

    with ProcessPoolExecutor(max_workers=max_processes) as executor:
        # execute functions in parallel
        return execute_with_executor(executor, functions)


def execute_with_executor(executor: Executor,
                          functions: List[Union[callable, Tuple[callable, tuple]]]
                          ) -> List[Future]:
    """
    Executes the given functions using the provided executor.

    Args:
        executor: The executor to use for parallel execution.
        functions: A list of functions or tuples of function and arguments.

    Returns:
        List of futures representing the execution of the functions.
    """

    futures = []
    for func in functions:
        try:
            if isinstance(func, tuple):
                f, args = func
                futures.append(executor.submit(f, *args))
            else:
                futures.append(executor.submit(func))
        except ValueError as err:
            raise ValueError(f"{type(executor).__name__}: {err}, arg: {func}")

    return futures