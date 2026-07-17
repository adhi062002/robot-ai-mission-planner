import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/augustin/robot-ai-mission-planner/install/robot_ai_mission_planner'
