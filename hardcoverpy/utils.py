def clean_api_key(api_key: str):
  if 'Bearer' in api_key:
      key = f'{api_key}'
  else:
      key = api_key.replace(' ', '')
      key = f'Bearer {key}'
  
  return key