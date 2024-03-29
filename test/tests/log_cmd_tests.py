from pavilion import commands
from pavilion import plugins
from pavilion.unittest import PavTestCase
from pavilion import schedulers
from pavilion.status_file import STATES
import argparse
import io
import time


class LogCmdTest(PavTestCase):

    def setUp(self):
        plugins.initialize_plugins(self.pav_cfg)

    def tearDown(self):
        plugins._reset_plugins()

    def test_log_arguments(self):
        log_cmd = commands.get_command('log')

        parser = argparse.ArgumentParser()
        log_cmd._setup_arguments(parser)

        # run a simple test
        test = self._quick_test()
        test.build()
        raw = schedulers.get_scheduler_plugin('raw')

        raw.schedule_test(self.pav_cfg, test)

        state = test.status.current().state
        end = time.time() + 1
        while ('ERROR' not in state and 'FAIL' not in state and
                state != STATES.COMPLETE and time.time() < end):
            time.sleep(.1)

        # test `pav log run test`
        args = parser.parse_args(['run', str(test.id)])
        self.assertEqual(args.test, test.id)

        out = io.StringIO()
        err = io.StringIO()

        result = log_cmd.run(self.pav_cfg, args, out_file=out, err_file=err)
        err.seek(0)
        out.seek(0)
        self.assertEqual(err.read(), '')
        self.assertEqual(out.read(), 'Hello World.\n')
        self.assertEqual(result, 0)

        # test `pav log build test`
        # note: echo-ing hello world should not require anything to be built
        out.truncate(0)
        err.truncate(0)
        args = parser.parse_args(['build', str(test.id)])
        log_cmd.run(self.pav_cfg, args, out_file=out, err_file=err)
        out.seek(0)
        err.seek(0)
        self.assertEqual(out.read(), '')

        # test `pav log kickoff test`
        # note: in general, kickoff.log should be an empty file
        out.truncate(0)
        err.truncate(0)
        args = parser.parse_args(['kickoff', str(test.id)])
        result = log_cmd.run(self.pav_cfg, args, out_file=out, err_file=err)
        out.seek(0)
        err.seek(0)
        self.assertEqual(out.read(), '')
        self.assertEqual(err.read(), '')
        self.assertEqual(result, 0)
