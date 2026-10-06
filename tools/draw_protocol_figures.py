"""Vector diagrams of the implemented protocol; no experiment data generated."""
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

OUT=Path(__file__).resolve().parents[1]/'figures'
plt.rcParams.update({'font.family':'DejaVu Sans','pdf.fonttype':42,'svg.fonttype':'none'})
def export(fig,name):
    for ext in ('pdf','svg'):fig.savefig(OUT/(name+'.'+ext),bbox_inches='tight',pad_inches=.08)
    svg=OUT/(name+".svg")
    svg.write_text("\n".join(line.rstrip() for line in svg.read_text().splitlines())+"\n",encoding="utf8")
    plt.close(fig)

fig,ax=plt.subplots(figsize=(7,7.5));ax.set(xlim=(0,10),ylim=(0,10));ax.axis('off')
def box(x,y,t,size=9):ax.text(x,y,t,ha='center',va='center',fontsize=size,bbox=dict(boxstyle='round,pad=.45',fc='#f3f5f7',ec='#34495e'))
def arrow(y,label,reverse=False):
    a,b=(8,2) if reverse else (2,8)
    ax.annotate('',xy=(b,y),xytext=(a,y),arrowprops=dict(arrowstyle='->',lw=1.2))
    ax.text(5,y+.12,label,ha='center',va='bottom',fontsize=8)
box(2,9.55,'ESP32 client');box(8,9.55,'Python server')
for x in (2,8):ax.plot([x,x],[.7,9.2],color='#777',ls='--',lw=.8)
box(2,8.6,'Generate ephemeral X25519\nand ML-KEM-768 keys\nHMAC the unsigned request',8)
arrow(7.7,'POST /handshake: 1,249-byte ClientHello')
box(8,6.8,'Verify request HMAC\nX25519 + ML-KEM encapsulation\nHKDF; generate SID\nHMAC request + unsigned response',8)
arrow(5.8,'HTTP response: 1,168-byte ServerHello',True)
box(2,4.9,'Verify transcript HMAC\nX25519; reject all-zero secret\nML-KEM decapsulation; HKDF',8)
arrow(3.65,'POST /api/telemetry: SID + IV + ciphertext + tag')
box(8,2.8,'Check counter; authenticate/decrypt\nUpdate counter after valid processing\nEncrypt acknowledgment',8)
arrow(1.75,'Encrypted acknowledgment',True)
ax.text(5,.65,'One application key-exchange request/response; TCP setup is separate.\nNo Finished flight; telemetry shares one key across directions and uses no AAD.\nRotate after 50 successful responses; three consecutive errors also end the session.',ha='center',va='center',fontsize=8)
export(fig,'handshake_sequence')

fig,ax=plt.subplots(figsize=(8,2.5));ax.set(xlim=(0,10),ylim=(0,3));ax.axis('off')
for x,t in [(1.6,'ESP32 / FreeRTOS\nX25519 + native ML-KEM-768\nmbedTLS AES-GCM'),(5,'Wi-Fi + HTTP/TCP\nPSK-authenticated exchange\nEncrypted telemetry'),(8.4,'Python / aiohttp\ncryptography + native ML-KEM\nIn-memory session state')]:
    ax.text(x,1.7,t,ha='center',va='center',fontsize=9,bbox=dict(boxstyle='round,pad=.6',fc='#f3f5f7',ec='#34495e'))
for a,b in [(3.1,3.5),(6.5,6.9)]:ax.annotate('',xy=(b,1.7),xytext=(a,1.7),arrowprops=dict(arrowstyle='<->',lw=1.3))
ax.text(5,.35,'Research testbed: public evaluation PSK, shared directional traffic key, no telemetry AAD.',ha='center',fontsize=8)
export(fig,'architecture_diagram')
print('Vector architecture and actual handshake diagrams generated.')
