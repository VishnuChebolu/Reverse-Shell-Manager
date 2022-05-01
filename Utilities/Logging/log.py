import sys

class Log():
    @staticmethod
    def _print(word):
        sys.stdout.write(word)
        sys.stdout.flush()

    @staticmethod
    def info(word):
        Log._print("\n\033[94m[~] {}\n\033[00m" .format(word))
        Log._print('\n')

    @staticmethod
    def warning(word):
        Log._print("\n\033[93m[!] {}\n\033[00m" .format(word))
        Log._print('\n')

    @staticmethod
    def error(word):
        Log._print("\n\033[91m[!] {}\n\033[00m" .format(word))
        Log._print('\n')

    @staticmethod
    def success(word):
        Log._print("\n\033[92m[+] {}\n\033[00m" .format(word))
        Log._print('\n')

    @staticmethod
    def query(word):
        Log._print("\n\033[93m[?] {}\n\033[00m" .format(word))
        Log._print('\n')


