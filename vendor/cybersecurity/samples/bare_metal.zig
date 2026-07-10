// FSOT code-genome sample — Zig bare-metal style.
const std = @import("std");

pub fn tritCollapse(a: i32, b: i32, c: i32) i32 {
    const min3 = @min(@min(a, b), c);
    const max3 = @max(@max(a, b), c);
    return a + b + c - min3 - max3;
}

pub fn main() !void {
    const out = tritCollapse(1, -1, 0);
    try std.io.getStdOut().writer().print("{d}\n", .{out});
}