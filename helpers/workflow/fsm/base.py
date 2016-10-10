# -*- coding: utf-8 -*-
"""
helpers.workflow.fsm.base

Workflow and state machine functions.

* created: 2013-10-17 Kevin Chan <kefin@makedostudio.com>
* updated: 2013-10-17 kchan

"""

from garage.logger import logger


class Transition(object):

    def __init__(self, src, dst_true, dst_false, action):
        """
        Initialize a transition object.

        :param src: src state
        :param dst_true: dst state if transition returns True
        :param dst_false: dst state if transition returns False
        """
        self.action = action
        self.src = src
        self.dst_true = dst_true
        self.dst_false = dst_false


class StateMachine(object):
    """
    Definition for a state machine.
    * this class implements a simple Moore Machine with finite states.
    * each state transition should define destinations for positive
      or negative results (returned by the action method associated
      with the transition).

    state and transition definitions should be a list of
    (source, dst_true, dst_false, action) tuples
    e.g.
    states = (
        ('initial', 'send', 'error', 'prep'),
        ('send', 'verify', 'error', 'send_message'),
        ('verify', 'completed', 'error', 'verify_message'),
    )

    example state machine class definition:

        class TestFsm(StateMachine):

            states = (
                ('initial', 'ready', 'error', 'prep'),
                ('ready', 'sent', 'error', 'send_message'),
                ('sent', 'completed', 'error', 'verify_message'),
                ('error', 'aborted', 'error', 'handle_error'),
            )

            initial = 'initial'
            final = ('completed', 'aborted',)

            def send_message(self):
                print "# sending message..."
                return True

            def verify_message(self):
                print "# verifying message..."
                return False

            def handle_error(self):
                print "# handle error..."
                return True

    """

    # state and transition definitions
    states = []

    # initial state
    initial = None

    # final states (list/tuple)
    final = []

    # use default transition handler
    # * if True, use default transition handler (returns True)
    use_default_transition_handler = True

    # debug
    # * if True, dump debug message to log file
    debug = False

    def __init__(self, **kwargs):
        """
        Initialize.
        """
        # set initial state
        self._current = self.initial

        # create transition table
        tmap = {}
        try:
            for entry in self.states:
                src, dst_true, dst_false, action = entry
                tmap[src] = Transition(*entry)
        except ValueError:
            tmap = {}
        self._transitions = tmap

        # store kwargs as attributes
        for k, v in kwargs.iteritems():
            if not k.startswith('_'):
                setattr(self, k, v)


    def current_state(self):
        """
        Get current state.
        """
        return self._current

    def is_state(self, state):
        """
        Test if state matches current state.
        """
        return state == self._current

    def is_final(self):
        """
        Test if curent state is accept state.
        """
        return not self._current or not self.final or self._current in self.final

    def default_transition(self):
        """
        Default transition handler.
        """
        return True

    def _msg(self, msg):
        """
        Dump debug message to log file.
        """
        if self.debug:
            logger().debug(msg)

    def run(self):
        """
        Run state machine.
        """
        self._msg('# state machine start...')
        self._msg('# current state: %s' % self._current)
        done = False
        while not done:
            if self.is_final():
                self._msg('# final state: %s' % self._current)
                done = True
            else:
                state = self._current
                if not state in self._transitions:
                    self._msg('# state not in transitions table: %s' % state)
                    done = True
                else:
                    self._msg('# * state %s is in transitions' % state)
                    transition = self._transitions[state]
                    action = transition.action
                    handler = getattr(self, action, None)
                    if callable(handler):
                        self._msg('# * triggering action: %s' % action)
                        result = handler()
                    elif self.use_default_transition_handler:
                        self._msg('# * using default transition')
                        result = self.default_transition()
                    else:
                        self._msg('# * no handler found for action: %s' % action)
                        result = False
                    self._msg('# > action result: %s' % result)
                    if result is True:
                        self._current = transition.dst_true
                    else:
                        self._current = transition.dst_false
                    self._msg('# state: %s' % self._current)
