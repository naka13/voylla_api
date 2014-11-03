import json

prod_stats = {}
prod_stats["clicks"] = 12
prod_stats["buys"] = 2
prod_stats = json.dumps(prod_stats)

print prod_stats
