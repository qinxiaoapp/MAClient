# coding:utf-8
from _prototype import plugin_prototype
from cross_platform import *
import time
# start meta
__plugin_name__ = '个排单砍MOD版,妹妹排行'
__author = 'Master'
__version__ = 0.4
__tip__ = '殴打妹妹排行插件已开启，如需关闭请移除plugins下的self_ranking_rocks'
hooks = {'EXIT__fairy_battle':10}
# extra cmd hook
extra_cmd = {'rbl':'rollback_log'}
# end meta
class plugin(plugin_prototype):
    def __init__(self):
        self.__name__ = __plugin_name__
        self.mac_instance = None
        self._ori_logfile = ''

    def fairy_floor(self,fairy):
        paramfl = 'check=1&race_type=%s&serial_id=%s&user_id=%s' % (
            fairy.race_type, fairy.serial_id, fairy.discoverer_id)
        resp, ct = self.mac_instance._dopost('exploration/fairy_floor', postdata = paramfl)
        if resp['error']:
            return None
        else:
            return ct.body.fairy_floor.explore.fairy

    def _rollback_log(self):
        self.logger.logfile.flush()
        self.logger.logfile.close()
        self.logger.logfile = self._ori_logfile
        self._ori_logfile = ''

    def EXIT__fairy_battle(self, *args, **kwargs):
        self.logger = args[0].logger
        if not self._ori_logfile:#不记录
            self.logger.logfile.flush()
            self._ori_logfile = self.logger.logfile
            self.logger.setlogfile('.IGF.log') 
        fairy=args[1]
        # this is for test only print(fairy.race_type)
        if fairy.race_type == '1' and fairy.time_limit != '0':
            print(du8("\n ----------发现野生的妹妹一只！进入无限殴打模式！！------------\n"))
            self.mac_instance = args[0]
            self.mac_instance.lastfairytime=0
            fairy=self.fairy_floor(fairy)
            if fairy.hp == '0' or fairy.time_limit == '0':
                self._rollback_log()
                return
            if self.mac_instance.player.bc['current']>=29:
                time.sleep(14)
                print(du8("\n -----------休息14秒 前方持续高能--------------- \n"))
                self.mac_instance._fairy_battle(fairy, carddeck = 'min', bt_type = 0)#0 -> EXPLORE_BATTLE 不用重新fairy_floor
            else:
                if not self.mac_instance.red_tea(silent = True):
                    _t = self.mac_instance.player.bc['interval_time'] * 2
                    print(du8("BC<29，%.1f分钟后再战ww" % (_t/60)))
                    time.sleep(_t)
                self.mac_instance._fairy_battle(fairy, carddeck = 'min', bt_type = 0)
        else:
            self._rollback_log()

def rollback_log(plugin_vals):
    def do(*args):
        plugin_vals['logger'].setlogfile('events_%s.log'%plugin_vals['loc'])
    return do

