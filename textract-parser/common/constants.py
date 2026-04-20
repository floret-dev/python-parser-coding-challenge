from dataclasses import dataclass

@dataclass(frozen=True)
class StoreKey:
    file_type = 'store.file_type'


store_key = StoreKey()
