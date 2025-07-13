from autogen_agentchat.conditions import TextMentionTermination

def stop_termination():
    termination_call = TextMentionTermination("STOP")
    return termination_call