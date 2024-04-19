from contextlib import contextmanager
from typing import Optional

from robocorp import log

from sema4ai.actions._protocols import IAction


def _log_before_action_run(task: IAction):
    log.start_task(
        task.name,
        task.module_name,
        task.filename,
        task.method.__code__.co_firstlineno + 1,
        getattr(task.method, "__doc__", ""),
    )


def _log_after_action_run(task: IAction):
    status = task.status
    log.end_task(task.name, task.module_name, status, task.message)


@contextmanager
def setup_cli_auto_logging(config: Optional[log.AutoLogConfigBase]):
    # This needs to be called before importing code which needs to show in the log
    # (user or library).

    from sema4ai.actions._hooks import after_task_run, before_task_run

    with log.setup_auto_logging(config):
        with before_task_run.register(_log_before_action_run), after_task_run.register(
            _log_after_action_run
        ):
            try:
                yield
            finally:
                log.close_log_outputs()