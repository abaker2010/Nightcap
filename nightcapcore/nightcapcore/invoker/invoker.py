from nightcapcore.command.command import Command


class Invoker:
    """

    The Invoker is associated with one or several commands. It sends a request
        to the command

    ...

    Attributes
    ----------


    Methods
    -------
        Accessible
        -------

        None Accessible
        -------

    """

    _on_start = None
    _on_finish = None

    def set_on_start(self, command: Command):
        self._on_start = command

    def set_on_finish(self, command: Command):
        self._on_finish = command

    def execute(self) -> None:
        """
        The Invoker does not depend on concrete command or receiver classes. The
        Invoker passes a request to a receiver indirectly, by executing a
        command.
        """

        if isinstance(self._on_start, Command):
            return self._on_start.execute()

        if isinstance(self._on_finish, Command):
            return self._on_finish.execute()
