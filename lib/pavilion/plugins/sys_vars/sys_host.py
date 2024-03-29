import subprocess
import pavilion.system_variables as system_plugins


class SystemHost(system_plugins.SystemPlugin):

    def __init__(self):
        super().__init__(
            plugin_name='sys_host', 
            description="The system (kickoff) hostname.",
            priority=self.PRIO_CORE,
            is_deferable=False, 
            sub_keys=None)

    def _get( self):
        """Base method for determining the system name."""

        name = subprocess.check_output(['hostname', '-s'])
        return name.strip().decode('UTF-8')
