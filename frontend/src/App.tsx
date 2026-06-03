import { DocsPage } from "@/pages/docs";
import { DiagnosisPage } from "@/pages/diagnosis";
import { HomePage } from "@/pages/home";
import { ModelsPage } from "@/pages/models";
import { useEffect } from "react";
import { Navigate, Route, Routes, useLocation } from "react-router-dom";

function ScrollToHash() {
  const location = useLocation();

  useEffect(() => {
    if (!location.hash) {
      window.scrollTo({ behavior: "smooth", top: 0 });
      return;
    }

    const target = document.querySelector(location.hash);
    target?.scrollIntoView({ behavior: "smooth", block: "start" });
  }, [location.pathname, location.hash]);

  return null;
}

export default function App() {
  return (
    <>
      <ScrollToHash />
      <Routes>
        <Route element={<HomePage />} path="/" />
        <Route element={<DiagnosisPage />} path="/diagnosis" />
        <Route element={<DocsPage />} path="/docs" />
        <Route element={<ModelsPage />} path="/models" />
        <Route element={<Navigate replace to="/" />} path="*" />
      </Routes>
    </>
  );
}
