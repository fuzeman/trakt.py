from threading import Condition, Lock


class Semaphore(object):
    def __init__(self, value=1):
        if value < 0:
            raise ValueError("semaphore initial value must be >= 0")

        self.__cond = Condition(Lock())
        self.__value = value

    def acquire(self, blocking=1):
        rc = False

        with self.__cond:
            while self.__value == 0:
                if not blocking:
                    break

                self.__cond.wait()
            else:
                self.__value = self.__value - 1

                rc = True

        return rc

    __enter__ = acquire

    def release(self):
        with self.__cond:
            self.__value = self.__value + 1
            self.__cond.notify()

    def release_multi(self, value):
        with self.__cond:
            self.__value = value
            self.__cond.notify_all()

    def __exit__(self, t, v, tb):
        self.release()
