import { describe, it, expect, test } from "vitest";

describe("Simple truthy test", () => {
  it("should expect true to equal true", () => {
    expect(true).toEqual(true);
  });
});

test("addition", () => {
  expect(1 + 1).toBe(2);
});
