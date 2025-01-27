import { Box, Button, Toolbar, Typography } from "@mui/material";
import { Divider } from "@mui/material";
import { AppBar } from "@mui/material";
import { useState, useEffect } from "react";
import { storage } from "./firebase";
import { v4 } from "uuid";
import { ref, uploadBytes, listAll, getDownloadURL } from "firebase/storage";
import { CircularProgress } from "@mui/material";

export const App = () => {
  const [selectedImage, setSelectedImage] = useState<FileList | null>(null);
  const [loading, setLoading] = useState(false);
  const [resultado, setResultado] = useState<string | null>(null);

  const uploadImage = async () => {
    if (selectedImage == null) return;
    setLoading(true);
    const fileRef = ref(storage, `lunares/${selectedImage[0].name + v4()}`);
    await uploadBytes(fileRef, selectedImage[0]);
    alert("imagen subida, procediendo a analizar");
    const imgurl = await getDownloadURL(fileRef);
    try {
      const response = await fetch("http://localhost:5000/predict", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ url: imgurl }),
      });
      const data = await response.json();
      console.log("Resultado:", data.clase);
      setResultado(data.clase);
    } catch (error) {
      console.error("Error al clasificar la imagen:", error);
    }
    setLoading(false);
  };

  return (
    <Box sx={{ alignItems: "center", justifyContent: "center" }}>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h3"></Typography>
        </Toolbar>
      </AppBar>

      <Typography variant="h1" textAlign={"center"}>
        DETECTOR DE CÁNCER DE PIEL
      </Typography>
      <Typography variant="body1" textAlign={"center"}>
        Proyecto final, materia: Seminario de Inteligencia artificial 2.
      </Typography>
      <Typography variant="body1" textAlign={"center"}>
        Equipo: Eduardo Rafael Pérez Flores y Jorge Ivan Reyes Arriaga
      </Typography>
      <Divider sx={{ border: "1px solid" }}></Divider>
      <center>
        <br></br>
        <input
          type="file"
          onChange={(event) => {
            setSelectedImage(event.target.files);
          }}
        ></input>
        <Button variant="outlined" onClick={uploadImage}>
          SUBIR IMAGEN
        </Button>
        <br></br>
        {loading ? (
          <>
            <CircularProgress color="success" />
          </>
        ) : (
          <></>
        )}
        {resultado && (
          <>
            {/* Mostrar una imagen dependiendo del resultado */}
            {resultado === "Potencialmente lunar" ? (
              <>
                <>
                  <Typography
                    variant="h6"
                    color="primary"
                    textAlign={"center"}
                    mt={2}
                  >
                    Resultado de la clasificación: {resultado}
                  </Typography>
                </>
                <img
                  src={"/assets/GoodEnding.jpg"}
                  alt="Potencialmente Lunar"
                  style={{ width: "300px", height: "300px", marginTop: "20px" }}
                />
                <audio autoPlay>
                  <source src="/assets/GoodEnding.mp3" type="audio/mp3" />
                </audio>
              </>
            ) : resultado === "Potencialmente Cancer" ? (
              <>
                <>
                  <Typography
                    variant="h6"
                    color="error"
                    textAlign={"center"}
                    mt={2}
                  >
                    Resultado de la clasificación: {resultado}
                  </Typography>
                </>
                <img
                  src={"/assets/badEnding.jpg"}
                  alt="Potencialmente Lunar"
                  style={{ width: "300px", height: "300px", marginTop: "20px" }}
                />
                <audio autoPlay>
                  <source src="/assets/badEnding.mp3" type="audio/mp3" />
                </audio>
              </>
            ) : null}
          </>
        )}
      </center>
    </Box>
  );
};
