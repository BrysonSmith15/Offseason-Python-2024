from ntcore import NetworkTableInstance, EventFlags, Event
import typing
from wpilib import reportWarning


class Tunable:
    nt_inst = NetworkTableInstance.getDefault().getTable()
    update_call: typing.Callable[[], []]
    value: typing.Any
    topic_name: str

    def __init__(self,
                 topic_type: type,
                 topic_name: str,
                 default_value=None,
                 call_on_update: typing.Callable[[], []] = lambda: ()):
        if default_value is None:
            default_value = topic_type()
        self.value = default_value
        self.topic_name = topic_name
        self.update_call = call_on_update
        self.nt_inst.addListener(topic_name, EventFlags.kValueAll, self.update)
        self.nt_inst.getTopic(topic_name).genericPublish(
            str(topic_type)).set(default_value)

    def get(self):
        return self.value

    def set(self, value) -> None:
        try:
            self.nt_inst.putValue(self.topic_name, value)
            self.value = value
        except Exception as e:
            if not self.nt_inst.putValue(self.topic_name, value):
                reportWarning(
                    f"Error thrown while getting update from \
                    {self.topic_name} with err {e} because of type clash")
            else:
                reportWarning(
                    f"Error thrown while getting update from \
                    {self.topic_name} with err {e}")

    def update(self, event: Event):
        try:
            self.value = event.data.value.value()
            self.update_call()
        except Exception as e:
            if not self.nt_inst.putValue(self.name, self.value):
                reportWarning(
                    f"Error thrown while getting update from \
                    {self.topic_name} with err {e} because of type clash")
            else:
                reportWarning(
                    f"Error thrown while getting update from \
                    {self.topic_name} with err {e}")
