import cProfile
import pstats
import sys
import StringIO

main_profiler = cProfile.Profile()
main_profiler.enable()
thread_profilers = []

def setprofile(thread):
  thread_profiler = cProfile.Profile()
  thread_profiler.enable()
  thread_profilers.append(thread_profiler)

def dump_stats():
  main_profiler.disable()
  s = StringIO.StringIO()
  main_stats = pstats.Stats(main_profiler, stream=s)
  for thread_profiler in thread_profilers:
    thread_stats = pstats.Stats(thread_profiler)
    main_stats.add(thread_stats)
  main_stats.sort_stats(2).print_stats()
  print "\n".join(s.getvalue().split("\n")[:50])
  main_profiler.enable()