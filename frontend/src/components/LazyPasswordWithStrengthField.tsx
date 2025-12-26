import { TextFieldProps } from "@mui/material/TextField";
import { lazy, Suspense } from "react";
import { FieldHookConfig } from "formik";
import PasswordField from "./PasswordField";
const PasswordWithStrengthField = lazy(
  () => import("./PasswordWithStrengthField"),
);
const LazyPasswordWithStrengthField = (
  props: FieldHookConfig<string> & TextFieldProps,
) => (
  <Suspense fallback={<PasswordField {...props} />}>
    <PasswordWithStrengthField {...props} />
  </Suspense>
);
export default LazyPasswordWithStrengthField;
