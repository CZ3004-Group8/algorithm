from algorithm.entities.commands.command import Command


class ScanCommand(Command):
    def __init__(self, time):
        super().__init__(time)

    def __str__(self):
        return f"ScanCommand(time={self.time})"

    __repr__ = __str__

    def process_one_tick(self, robot):
        if self.total_ticks == 0:
            return

        self.tick()

    def apply_on_pos(self, curr_pos):
        pass
