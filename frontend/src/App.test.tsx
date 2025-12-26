import { expect, test, it, describe } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import App from "./App";

describe("<App />", () => {
  it("is first test", () => {
    render(<App />);
    // fireEvent.click(screen.getByRole("button"));
    // expect(screen.getByText(/count is 1/i)).toBeInTheDocument();
  });
});

test("addition", () => {
  expect(1 + 1).toBe(2);
});
