from dict_hash import sha256

class NightcapHash():
    def __init__(self) -> None:
        pass

    def hash_dict(self, o: dict):
        try: 
            return sha256(o)
        except Exception as e:
            raise Exception(f"ERROR GENERATING HASH :: {e}")