from os import environ

def get_env_var( var_name: str ):
  return environ.get( var_name )
