import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { App } from "./App";
import { createTheme, CssBaseline, ThemeProvider } from "@mui/material";

const theme = createTheme({
  palette: {
    mode: "light",
    primary: {
      main: "#349c00",
    },
    secondary: {
      main: "#f50057",
    },
    text: {
      primary: "rgba(255,255,255,0.87)",
    },
    background: {
      default: "#303030",
      paper: "#424242",
    },
  },
});

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <ThemeProvider theme={theme}>
      <CssBaseline></CssBaseline>
      <App />
    </ThemeProvider>
  </StrictMode>
);
