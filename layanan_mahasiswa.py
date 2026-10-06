"""
Sistem Antrean Layanan Administrasi Mahasiswa
- Antrean   : Queue (FIFO) diimplementasikan dengan Doubly Linked List
- Undo      : Stack (LIFO) diimplementasikan dengan list Python (array dinamis)
"""


# ======================= QUEUE =======================
class Node:
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None


class Queue:
    """Antrean FIFO. front = yang paling depan, rear = yang paling belakang."""

    def __init__(self):
        self.front = None
        self.rear = None
        self.size = 0

    # ---- operasi utama antrean (semua O(1)) ----
    def is_empty(self):
        return self.front is None

    def enqueue(self, data):
        """Tambah mahasiswa di belakang antrean."""
        node = Node(data)
        if self.is_empty():
            self.front = self.rear = node
        else:
            node.prev = self.rear
            self.rear.next = node
            self.rear = node
        self.size += 1

    def dequeue(self):
        """Layani (ambil) mahasiswa paling depan."""
        if self.is_empty():
            return None
        data = self.front.data
        self.front = self.front.next
        if self.front is None:
            self.rear = None
        else:
            self.front.prev = None
        self.size -= 1
        return data

    def peek(self):
        """Lihat mahasiswa paling depan tanpa menghapus."""
        return None if self.is_empty() else self.front.data

    # ---- operasi khusus untuk keperluan Undo (O(1)) ----
    def _add_front(self, data):
        """Mengembalikan mahasiswa ke posisi paling depan (membatalkan 'layani')."""
        node = Node(data)
        if self.is_empty():
            self.front = self.rear = node
        else:
            node.next = self.front
            self.front.prev = node
            self.front = node
        self.size += 1

    def _remove_rear(self):
        """Menghapus mahasiswa paling belakang (membatalkan 'tambah')."""
        if self.is_empty():
            return None
        data = self.rear.data
        self.rear = self.rear.prev
        if self.rear is None:
            self.front = None
        else:
            self.rear.next = None
        self.size -= 1
        return data

    def to_list(self):
        hasil, cur = [], self.front
        while cur:
            hasil.append(cur.data)
            cur = cur.next
        return hasil


# ======================= STACK =======================
class Stack:
    """Tumpukan LIFO. Ujung list = top."""

    def __init__(self):
        self._items = []

    def is_empty(self):
        return len(self._items) == 0

    def push(self, item):      # O(1) amortized
        self._items.append(item)

    def pop(self):             # O(1)
        return None if self.is_empty() else self._items.pop()

    def peek(self):            # O(1)
        return None if self.is_empty() else self._items[-1]

    def to_list(self):
        return list(self._items)


# ================= SISTEM LAYANAN ====================
class LayananMahasiswa:
    def __init__(self):
        self.antrean = Queue()
        self.riwayat = Stack()   # stack aktivitas untuk Undo

    def tambah_mahasiswa(self, nama):
        self.antrean.enqueue(nama)
        self.riwayat.push(("TAMBAH", nama))
        print(f"[TAMBAH ] {nama} masuk antrean")

    def layani_mahasiswa(self):
        if self.antrean.is_empty():
            print("[LAYANI ] Antrean kosong")
            return None
        nama = self.antrean.dequeue()
        self.riwayat.push(("LAYANI", nama))
        print(f"[LAYANI ] {nama} dilayani")
        return nama

    def lihat_terdepan(self):
        nama = self.antrean.peek()
        print(f"[PEEK   ] Terdepan: {nama}")
        return nama

    def antrean_kosong(self):
        return self.antrean.is_empty()

    def undo(self):
        if self.riwayat.is_empty():
            print("[UNDO   ] Tidak ada aktivitas untuk dibatalkan")
            return
        aksi, nama = self.riwayat.pop()
        if aksi == "TAMBAH":
            self.antrean._remove_rear()        # batalkan penambahan
            print(f"[UNDO   ] Batalkan TAMBAH {nama}")
        else:
            self.antrean._add_front(nama)      # kembalikan ke depan
            print(f"[UNDO   ] Batalkan LAYANI {nama}")

    def tampilkan(self):
        print(f"          Antrean (depan->belakang): {self.antrean.to_list()}")
        print(f"          Stack Undo (bawah->top)  : {self.riwayat.to_list()}\n")


# ===================== DEMO ==========================
if __name__ == "__main__":
    s = LayananMahasiswa()
    print("Antrean kosong?", s.antrean_kosong(), "\n")

    s.tambah_mahasiswa("Rizky");  s.tampilkan()
    s.tambah_mahasiswa("Sara");   s.tampilkan()
    s.tambah_mahasiswa("Tina");   s.tampilkan()
    s.lihat_terdepan();           print()
    s.layani_mahasiswa();         s.tampilkan()   # Rizky
    s.tambah_mahasiswa("Umar");   s.tampilkan()
    s.layani_mahasiswa();         s.tampilkan()   # Sara
    s.tambah_mahasiswa("Vina");   s.tampilkan()
    s.undo();                     s.tampilkan()   # batalkan tambah Vina
    s.undo();                     s.tampilkan()   # batalkan layani Sara

    print("=== HASIL AKHIR ===")
    s.tampilkan()
    print("Antrean kosong?", s.antrean_kosong())