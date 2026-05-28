from dataclasses import dataclass

@dataclass(frozen=True)
class StoreKey:
    file_type = 'store.file_type'

@dataclass(frozen=True)
class Distributor:
    unfi = 'UNFI',
    kehe = 'KeHE'

store_key = StoreKey()
distributor = Distributor()