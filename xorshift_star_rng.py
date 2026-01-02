import time
import sys

class XorShiftStar64:
    def __init__(self, seed=None):
        self.MASK = 0xFFFFFFFFFFFFFFFF
        
        if seed is None:
            self.state = int(time.time_ns()) & self.MASK
        else:
            self.state = seed & self.MASK
            
        if self.state == 0:
            self.state = 0x1234567890ABCDEF

    def next_u64(self):
        x = self.state
        x ^= (x >> 12) & self.MASK
        x ^= (x << 25) & self.MASK
        x ^= (x >> 27) & self.MASK
        self.state = x & self.MASK
        return (x * 0x2545F4914F6CDD1D) & self.MASK

    def randint(self, min_val, max_val):
        if min_val > max_val:
            return min_val
        return min_val + (self.next_u64() % (max_val - min_val + 1))

    def random(self):
        return (self.next_u64() >> 11) / (1 << 53)

if __name__ == "__main__":
    user_seed = None
    if len(sys.argv) > 1:
        try:
            user_seed = int(sys.argv[1])
        except ValueError:
            print(f"Hata: '{sys.argv[1]}' geçerli bir tamsayı değil.")
            sys.exit(1)

    rng = XorShiftStar64(user_seed)
    
    print("XorShift* (Star) Başlatıldı.")
    if user_seed is not None:
        print(f"Kullanılan Tohum (Seed): {user_seed} (Sabit Çıktı Modu)")
    else:
        print(f"Kullanılan Tohum (Seed): ZAMAN TABANLI (Rastgele Mod)")
        print(f"Gerçek Seed Değeri: {rng.state} (Not alınırsa tekrar üretilebilir)")
    
    print("\nİlk 5 Sayı (Hex ve Decimal):")
    for i in range(5):
        val = rng.next_u64()
        print(f"{i+1}) {val:#018x} -> {val}")
