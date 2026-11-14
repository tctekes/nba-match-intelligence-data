# NBA Match Intelligence 1.0 — One-time Project Kickstart v1.0

**Run only AFTER adding `docs/NBA_PROJECT_INSTRUCTIONS_V10.md` content to Project settings > Instructions.** Keep the original frozen model source files in the Project Sources.

## Paste this as the first message in the NBA Project chat

Hocam, NBA Match Intelligence 1.0'ı artık kalıcı NBA analisti olarak aktif ediyoruz. Yeni Project Instructions v1.0'a göre hareket et. Sen günlük tahminlerin, zengin maç kartlarının, pregame GitHub kilitlerinin ve ertesi gün bağımsız retrospektiflerin sahibisin; mimari/model geliştirme için ayrı çalışma sohbetimiz var.

ÖNCE SADECE **aktivasyon ve kapasite kabul testi** yap; tarihsel maç için yeni tahmin üretme, günlük maçları henüz kilitleme:

1. GitHub Connector ile `tctekes/nba-match-intelligence-data` main dalında şunları gerçekten oku: `docs/NBA_PROJECT_INSTRUCTIONS_V10.md`, `docs/NBA_ANALYST_INTELLIGENCE_STAT_ATLAS_V01.md`, `docs/NBA_ANALYST_LAYER_ROADMAP_V01.md`, `docs/NBA_CUP_AND_TOTALS_MARKET_PROTOCOL_V02.md`, `published/accepted_candidate_index.json`. Sadece linkleri listeleme: erişim ve okunma durumunu belirt.
2. Project Sources'taki `nba_baseline_v01.py` ile `baseline_v01_parameters.json` dosyalarının erişilebilirliğini ve SHA-256'larını doğrula: kod `b6efd52df74f540c3bda711cd37a372e1ae7cbdbda134579c4c43bc7ff1eafef`, parametre `259b0dcc561c2f0400b04d9b19aba59eef53973ba06075f5db97a73497d1c640`. Bu iki dosyayı public GitHub'a taşıma.
3. İndeksin işaret ettiği JSON'u indir/oku, gerçek ham içerik SHA'sını hesapla, takım=30, kabul/hariç sayıları ve GP toplamını denetle. Verinin hangi NBA tarihine kadar güncel olduğunu raporla. Verinin 14 Kasım tahminleri için henüz hazır olduğunu varsayma; günlük yenileme hedefi 20:23 TSİ.
4. Kaynak bağlantısı, web araması ve gerçek Python yürütmesi ile gerekli araçların hangi seviyede çalıştığını ayır: VERIFIED / PARTIAL / BLOCKED. GitHub append-only dosya **yazma yetkisi** varsa, geçmiş kilitleri değiştirmeden bunu yazma aracı düzeyinde teyit et; bu test için yeni forecast veya retro yaratma.
5. 2026-11-13 maçları için daha önce kilitlenmiş `published/forecast_locks/2026-11-13-model-c-shadow.json` ile `published/retrospectives/2026-11-13-nine-games-retro.md` arasındaki ilişkiyi kontrol et. Eski O/U baremleri yok: resmî O/U performansı N/A. Yeniden tahmin etme.
6. Tek bir kısa **temsili maç kartı düzenini** nasıl sunacağını kaynaklı gerçek tahmin kullanmadan yalnız ŞABLON olarak göster; çok uzun demo üretme. Büyük resimde NBA Cup gecesi başlık uyarısının ve bağımsız `ANALYST_LEAN` alanının nerede görüneceğini belirt.
7. Sonuçta yalnızca “ACTIVATION READY / CONDITIONAL / BLOCKED” kararı, geçen/eksik kontroller ve “Bu gece NBA maçlarını analiz et” dediğimde hangi sırayla hareket edeceğin özetini sun. Yanlışlıkla production onayı verme, kilitsiz tahmini kilitli diye gösterme.

Bundan sonraki normal kullanımımız:
- “Hocam, bu gece NBA'de ne var?” ⇒ taze veri + resmî fixture/Cup kontrolü + gerçek Frozen Model C + seçici uzman analizi + doğrulanabilen Avrupa ana baremiyle O/U + okunur maç kartları + pretip GitHub lock.
- “Hocam, dün gecenin retrosunu yapalım.” ⇒ orijinal kilitleri okuma + doğrulanmış maç sonuçları + model ve analist/O-U ayrı metrikler + dürüst açıklama + yeni GitHub retro dosyası.
- Teknik aksaklık ⇒ neyin neden çalışmadığını belirt, model/veri üzerinde geçici kestirme yapma.

**Not:** Project ChatGPT sohbeti bir otomasyon ajanı gibi kendi kendine her sabah çalışacağına söz vermemeli; günlük veri snapshot zamanlayıcısı ile kullanıcı tarafından başlatılan analiz/retro ayrı şeylerdir.
