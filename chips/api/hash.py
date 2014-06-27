import hashlib
def dict_to_hash(the_dict):
   if not len(the_dict):
       return ""
   the_hash = hashlib.md5()
   values = sorted(the_dict.values())
   for value in values:
       the_hash.update(str(value))
   return str(the_hash.hexdigest())

assert dict_to_hash({}) == ""
assert dict_to_hash({"a":1, "b":2}) == dict_to_hash({"a":1, "c":2})
assert dict_to_hash({"a":1, "b":2.0}) == dict_to_hash({"a":1, "c":2.0})
assert dict_to_hash({"a":1, "b":2}) != dict_to_hash({"a":1, "c":2.0})
