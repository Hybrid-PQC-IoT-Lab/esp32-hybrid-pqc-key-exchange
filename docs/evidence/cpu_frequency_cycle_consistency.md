# Runtime CPU-Frequency and CPU-Cycle Consistency Evidence

## 1. System Clock Configuration
The ESP32-D0WD-V3 SoC contains dual Xtensa LX6 cores with a maximum rated frequency of 240 MHz. The n=100 UART boot log explicitly records ESP-IDF v5.5 and `cpu freq: 160000000 Hz`. The original full sdkconfig is not archived. The corrected `sdkconfig.defaults` explicitly requests **160 MHz**:

```ini
# Requested in firmware/sdkconfig.defaults
CONFIG_ESP_DEFAULT_CPU_FREQ_MHZ_160=y
CONFIG_ESP_DEFAULT_CPU_FREQ_MHZ=160
```

This frequency is synthesized from the 40 MHz onboard crystal oscillator via the main PLL ($480\text{ MHz} / 3 = 160\text{ MHz}$), driving the internal CCOUNT (cycle counter) register at exactly:
$$f_{\text{CPU}} = 160\text{ MHz} = 160 \times 10^6 \text{ cycles/second} = 160 \text{ cycles/\mu s}$$

## 2. Mathematical Consistency Verification
To establish empirical consistency between measured execution time ($\Delta t$, in microseconds or milliseconds) and hardware CPU cycles captured via `esp_cpu_get_cycle_count()`, we evaluate the ratio:
$$f_{\text{eff}} = \frac{\Delta\text{Cycles}}{\Delta t}$$

### A. Raw Testbed Log Evidence (from `data/raw_logs/custom_pqc_usb_serial.txt`)
| Operation | Measured Time ($\mu$s) | CPU Cycles | Calculated Frequency ($f_{\text{eff}}$) | Ratio to Nominal (160 MHz) |
|---|---|---|---|---|
| **X25519 KeyGen** | $302,989\,\mu\text{s}$ | $48,476,981$ | **159.996 MHz** | 0.99998 |
| **X25519 Shared Secret** | $155,923\,\mu\text{s}$ | $24,946,960$ | **159.995 MHz** | 0.99997 |
| **ML-KEM-768 KeyGen** | $14,164\,\mu\text{s}$ | $2,266,200$ | **159.997 MHz** | 0.99998 |
| **ML-KEM-768 Decapsulation** | $18,512\,\mu\text{s}$ | $2,961,717$ | **159.989 MHz** | 0.99993 |

### B. Archived n=100 intervals

Reanalysis gives mean latency 616.7478 ms and mean elapsed CCOUNT 100,330,347.16.
These are different timing windows: latency sums keygen and handshake phases;
CCOUNT also spans intervening packing, logging and heap sampling. Their ratio
must not be treated as a measured clock-frequency discrepancy or isolated CPU cost.
The earlier unrelated primitive-average table has been withdrawn from this note.

## 3. Scope

The boot log establishes the configured clock for the archived campaign. The
primitive examples above are separate observations compatible with 160 MHz.
They do not validate all builds, compiler options, or a universal 99.99% agreement.
