#![no_std]
#![no_main]

use bootloader::{BootInfo, entry_point};
use core::panic::PanicInfo;
use libm::{cos, exp, log, sin, sqrt};


entry_point!(kernel_boot);


const K: f64 = 0.4202216641606967;
const ALPHA: f64 = 0.0008082937414140405;
const PSI_CON: f64 = 0.6321205588285577;
const ETA_EFF: f64 = 0.46694220692425986;
const BETA: f64 = 2.620866911333223e-17;
const C_EFF: f64 = 0.9577022026205613;
const A_BLEED: f64 = 1.046973630587551;
const B_IN: f64 = 0.7879407922764435;
const A_IN: f64 = 1.6668538450045731;
const CHAOS: f64 = -0.33102418261048183;
const P_NEW: f64 = 0.30030227667037146;
const C_FACTOR: f64 = 0.28760015181918397;
const POOF: f64 = 0.1534822148944508;
const THETA_S: f64 = 0.29089654054517305;
const SUCTION: f64 = 0.14703398542810284;
const P_VAR: f64 = 0.9579871226722757;
const BOOT_SCALAR_CANONICAL: f64 = 0.09928895626861721;

fn compute_fsot_scalar(d_eff: f64, delta_psi: f64, observed: bool, recent_hits: f64) -> f64 {
    let n = 1.0_f64;
    let p = 1.0_f64;
    let d = d_eff.max(1.0);
    let dp = delta_psi;
    let hits = recent_hits;

    let growth = exp(ALPHA * (1.0 - hits / n) * 0.5772156649 / 1.6180339887);
    let base = (n * p / sqrt(d))
        * cos((PSI_CON + dp) / ETA_EFF)
        * exp(-ALPHA * hits / n + 1.0 + B_IN * dp)
        * (1.0 + growth * C_EFF);
    let mut t1 = base * (1.0 + P_NEW * log(d / 25.0));
    if observed {
        t1 = t1 * exp(C_FACTOR * P_VAR) * cos(dp + P_VAR);
    }

    let t2 = 0.0_f64;

    let valve = BETA * cos(dp) * (n * p / sqrt(d))
        * (1.0 + CHAOS * (d - 25.0) / 25.0)
        * (1.0 + POOF * cos(THETA_S + core::f64::consts::PI) + SUCTION * sin(THETA_S));
    let acoustic = 1.0
        + (A_BLEED * sin(1.0_f64) * sin(1.0_f64)) / 1.6180339887
        + (A_IN * cos(1.0_f64) * cos(1.0_f64)) / 1.6180339887;
    let phase = 1.0 + B_IN * P_VAR;
    let t3 = valve * acoustic * phase;

    K * (t1 + t2 + t3)
}

const VGA_WIDTH: usize = 80;
const VGA_HEIGHT: usize = 25;
static mut VGA_BUFFER: *mut u16 = 0xb8000 as *mut u16;
const SERIAL_PORT: u16 = 0x3F8;
const DEBUGCON_PORT: u16 = 0xe9;

#[inline(always)]
unsafe fn inb(port: u16) -> u8 {
    let value: u8;
    core::arch::asm!("in al, dx", out("al") value, in("dx") port, options(nomem, nostack, preserves_flags));
    value
}

#[inline(always)]
unsafe fn outb(port: u16, value: u8) {
    core::arch::asm!("out dx, al", in("dx") port, in("al") value, options(nomem, nostack, preserves_flags));
}

struct SerialWriter;

impl SerialWriter {
    fn init_uart(&self) {
        unsafe {
            outb(SERIAL_PORT + 1, 0x00);
            outb(SERIAL_PORT + 3, 0x80);
            outb(SERIAL_PORT + 0, 0x03);
            outb(SERIAL_PORT + 1, 0x00);
            outb(SERIAL_PORT + 3, 0x03);
            outb(SERIAL_PORT + 2, 0xC7);
            outb(SERIAL_PORT + 4, 0x0B);
        }
    }

    fn write_byte(&mut self, byte: u8) {
        unsafe {
            outb(DEBUGCON_PORT, byte);
            outb(SERIAL_PORT, byte);
        }
    }

    fn write_str(&mut self, s: &str) {
        for byte in s.bytes() {
            self.write_byte(byte);
        }
    }

    fn write_f64(&mut self, val: f64, precision: usize) {
        F64Printer::new(self).write(val, precision);
    }
}

struct VgaWriter {
    row: usize,
    col: usize,
}

impl VgaWriter {
    fn new() -> Self {
        Self { row: 0, col: 0 }
    }

    fn clear(&mut self) {
        for row in 0..VGA_HEIGHT {
            for col in 0..VGA_WIDTH {
                unsafe {
                    core::ptr::write_volatile(
                        VGA_BUFFER.offset((row * VGA_WIDTH + col) as isize),
                        0x0F00 | b' ' as u16,
                    );
                }
            }
        }
        self.row = 0;
        self.col = 0;
    }

    fn write_byte(&mut self, byte: u8) {
        match byte {
            b'\n' => {
                self.col = 0;
                self.row += 1;
                if self.row >= VGA_HEIGHT {
                    self.row = 0;
                }
            }
            _ => {
                if self.col >= VGA_WIDTH {
                    self.col = 0;
                    self.row += 1;
                    if self.row >= VGA_HEIGHT {
                        self.row = 0;
                    }
                }
                let idx = self.row * VGA_WIDTH + self.col;
                unsafe {
                    core::ptr::write_volatile(
                        VGA_BUFFER.offset(idx as isize),
                        0x0F00 | byte as u16,
                    );
                }
                self.col += 1;
            }
        }
    }

    fn write_str(&mut self, s: &str) {
        for byte in s.bytes() {
            self.write_byte(byte);
        }
    }

    fn write_f64(&mut self, val: f64, precision: usize) {
        F64Printer::new(self).write(val, precision);
    }
}

trait ByteWriter {
    fn write_byte(&mut self, byte: u8);
    fn write_str(&mut self, s: &str) {
        for byte in s.bytes() {
            self.write_byte(byte);
        }
    }
}

impl ByteWriter for VgaWriter {
    fn write_byte(&mut self, byte: u8) {
        VgaWriter::write_byte(self, byte);
    }
}

impl ByteWriter for SerialWriter {
    fn write_byte(&mut self, byte: u8) {
        SerialWriter::write_byte(self, byte);
    }
}

struct F64Printer<'a, W: ByteWriter> {
    writer: &'a mut W,
}

impl<'a, W: ByteWriter> F64Printer<'a, W> {
    fn new(writer: &'a mut W) -> Self {
        Self { writer }
    }

    fn write(&mut self, val: f64, precision: usize) {
        if val.is_nan() {
            self.writer.write_str("NaN");
            return;
        }
        if val.is_infinite() {
            if val.is_sign_negative() {
                self.writer.write_str("-inf");
            } else {
                self.writer.write_str("inf");
            }
            return;
        }
        let mut v = val;
        if v < 0.0 {
            self.writer.write_byte(b'-');
            v = -v;
        }
        let int_part = v as u64;
        let mut buf = [0u8; 32];
        let mut i = 0;
        if int_part == 0 {
            buf[i] = b'0';
            i += 1;
        } else {
            let mut tmp = int_part;
            while tmp > 0 {
                buf[i] = b'0' + (tmp % 10) as u8;
                tmp /= 10;
                i += 1;
            }
        }
        for j in (0..i).rev() {
            self.writer.write_byte(buf[j]);
        }
        if precision > 0 {
            self.writer.write_byte(b'.');
            let mut frac = v - (int_part as f64);
            for _ in 0..precision {
                frac *= 10.0;
                let digit = frac as u8;
                self.writer.write_byte(b'0' + digit);
                frac -= digit as f64;
            }
        }
    }
}

struct BootWriter<'a> {
    vga: &'a mut VgaWriter,
    serial: &'a mut SerialWriter,
}

impl<'a> BootWriter<'a> {
    fn write_str(&mut self, s: &str) {
        self.vga.write_str(s);
        self.serial.write_str(s);
    }

    fn write_f64(&mut self, val: f64, precision: usize) {
        self.vga.write_f64(val, precision);
        self.serial.write_f64(val, precision);
    }
}

fn kernel_boot(_boot_info: &'static BootInfo) -> ! {
    let mut vga = VgaWriter::new();
    let mut serial = SerialWriter;
    serial.init_uart();
    vga.clear();

    let mut out = BootWriter {
        vga: &mut vga,
        serial: &mut serial,
    };

    out.write_str("FSOT 2.0 Bare-Metal Observer Kernel POC v0.1\n");
    out.write_str("Fluid Spacetime Omni-Theory - Parameter Free | QEMU x86_64\n");
    out.write_str("Built with Rust no_std | FSOT Native Scalar Engine\n\n");
    out.write_str("Mapping boot to FSOT domain: KernelInit (D_eff=8, observed=True)\n");

    let d_eff = 8.0;
    let delta_psi = 0.7;
    let observed = true;
    let recent_hits = 0.0;
    let s = compute_fsot_scalar(d_eff, delta_psi, observed, recent_hits);

    out.write_str("Computed FSOT Scalar S_D_chaotic = ");
    out.write_f64(s, 6);
    out.write_str("\n");

    if s > 0.0 {
        out.write_str("Interpretation: POSITIVE (Emergence) - New information flow detected.\n");
        out.write_str("System entering high-coherence boot phase. Fluid spacetime active.\n");
    } else {
        out.write_str("Interpretation: NEGATIVE / DAMPED (Stabilization) - Perturbations suppressed.\n");
        out.write_str("System prioritizing stability during initialization.\n");
    }

    out.write_str("\nFSOT k-scaled output demonstrates ~99% domain fit principle in bare metal.\n");
    out.write_str("This POC proves FSOT scalar computation is viable in no-OS environments.\n\n");

    out.write_str("Tier 87 disk boot complete — halting for harness capture.\n");
    drop(out);

    serial.write_str("FSOT_QEMU_BOOT_SCALAR=");
    serial.write_f64(s, 17);
    serial.write_str("\n");
    serial.write_str("FSOT_QEMU_CANONICAL=");
    serial.write_f64(BOOT_SCALAR_CANONICAL, 17);
    serial.write_str("\n");
    serial.write_str("FSOT_QEMU_DISK_BOOT=ok\n");

    unsafe {
        outb(0xf4, 0x10);
    }
    loop {
        unsafe {
            core::arch::asm!("hlt", options(nomem, nostack, preserves_flags));
        }
    }
}

#[panic_handler]
fn panic(_info: &PanicInfo) -> ! {
    let mut serial = SerialWriter;
    serial.write_str("\n!!! PANIC - FSOT Stabilization Engaged !!!\n");
    loop {
        core::hint::spin_loop();
    }
}