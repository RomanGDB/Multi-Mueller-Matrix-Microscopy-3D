
// =====================================================
// FIJI MACRO
//
// HYPERSTACK:
//
// C = Canal
// Z = Propiedad física
// T = Distancia focal
//
// PROPIEDADES:
// Z1 = S0_pol
// Z2 = PoD
// Z3 = D
// Z4 = LR
// Z5 = OA
// Z6 = S0_uv
// Z7 = DoLP
// Z8 = AoLP
//
// Los archivos inexistentes quedan en negro.
// Los canales se detectan en todos los focos.
// =====================================================


// =====================================================
// ELEGIR CARPETA
// =====================================================

base = getDirectory("Elegir carpeta muestra");


// =====================================================
// PROPIEDADES Y ORDEN
// =====================================================

propFiles = newArray(
    "S0_POL.png",
    "PoD.png",
    "D.png",
    "LR.png",
    "OA.png",
    "S0_UV.png",
    "DoLP.png",
    "AoLP.png"
);

nProps = propFiles.length;


// =====================================================
// DETECTAR FOCOS
// =====================================================

zFolders = getFileList(base);
zList = newArray();

for (i = 0; i < zFolders.length; i++) {

    if (File.isDirectory(base + zFolders[i])) {
        zList = Array.concat(zList, zFolders[i]);
    }
}

Array.sort(zList);

nZ = zList.length;

if (nZ == 0)
    exit("No se encontraron carpetas de foco.");


// =====================================================
// DETECTAR TODOS LOS CANALES
// =====================================================

channelList = newArray();

for (z = 0; z < nZ; z++) {

    zName = zList[z];

    folders = getFileList(base + zName);

    for (i = 0; i < folders.length; i++) {

        folderPath = base + zName + "/" + folders[i];

        if (File.isDirectory(folderPath)) {

            found = false;

            for (j = 0; j < channelList.length; j++) {

                if (channelList[j] == folders[i])
                    found = true;
            }

            if (!found)
                channelList = Array.concat(channelList, folders[i]);
        }
    }
}

Array.sort(channelList);

nChannels = channelList.length;

if (nChannels == 0)
    exit("No se encontraron canales.");


// =====================================================
// BUSCAR PRIMERA IMAGEN EXISTENTE
// PARA DETERMINAR DIMENSIONES
// =====================================================

W = 0;
H = 0;
foundImage = false;

for (z = 0; z < nZ && !foundImage; z++) {

    for (c = 0; c < nChannels && !foundImage; c++) {

        for (p = 0; p < nProps && !foundImage; p++) {

            imgPath = base + zList[z] + "/" +
                      channelList[c] + "/" +
                      propFiles[p];

            if (File.exists(imgPath)) {

                open(imgPath);

                W = getWidth();
                H = getHeight();

                close();

                foundImage = true;
            }
        }
    }
}

if (!foundImage)
    exit("No se encontraron imágenes de propiedades.");


// =====================================================
// CREAR HYPERSTACK
// =====================================================

run("New Hyperstack...",
    "name=Polarimetric_HyperStack " +
    "type=RGB " +
    "width=" + W + " " +
    "height=" + H + " " +
    "channels=" + nChannels + " " +
    "slices=" + nProps + " " +
    "frames=" + nZ + " " +
    "display=Color");

stackID = getImageID();


// =====================================================
// RECORRER TODAS LAS POSICIONES
// =====================================================

totalFound = 0;
totalMissing = 0;

for (z = 0; z < nZ; z++) {

    zName = zList[z];

    for (p = 0; p < nProps; p++) {

        propName = propFiles[p];

        for (c = 0; c < nChannels; c++) {

            canal = channelList[c];

            imgPath = base + zName + "/" +
                      canal + "/" +
                      propName;

            print(
                "Canal: " + canal +
                " | Propiedad: " + propName +
                " | Foco: " + zName
            );

            // =========================================
            // POSICIÓN EN HYPERSTACK
            // =========================================

            selectImage(stackID);

            Stack.setPosition(
                c + 1,
                p + 1,
                z + 1
            );

            // =========================================
            // COMPROBAR EXISTENCIA
            // =========================================

            if (File.exists(imgPath)) {

                open(imgPath);

                sourceID = getImageID();

                // Comprobar dimensiones

                if (getWidth() != W || getHeight() != H) {

                    close();

                    totalMissing++;

                    print("ERROR: Dimensiones incompatibles: " + imgPath);

                } else {

                    // =================================
                    // CONVERTIR A RGB
                    // =================================

                    run("RGB Color");

                    // =================================
                    // ETIQUETA
                    // =================================

                    setFont("SansSerif", 18);

                    setColor("black");

                    makeRectangle(0, 0, 500, 100);
                    run("Fill");

                    setColor("white");

                    drawString("CANAL: " + canal, 15, 25);
                    drawString("PROPIEDAD: " + propName, 15, 52);
                    drawString("FOCO: " + zName, 15, 79);

                    // =================================
                    // COPIAR Y PEGAR
                    // =================================

                    run("Select All");
                    run("Copy");

                    selectImage(stackID);

                    Stack.setPosition(
                        c + 1,
                        p + 1,
                        z + 1
                    );

                    run("Paste");
                    run("Select None");

                    // =================================
                    // CERRAR ORIGINAL
                    // =================================

                    selectImage(sourceID);
                    close();

                    selectImage(stackID);

                    totalFound++;
                }

            } else {

                // Plano vacío: permanece negro

                totalMissing++;

            }
        }
    }
}


// =====================================================
// POSICIÓN INICIAL
// =====================================================

selectImage(stackID);

Stack.setPosition(1, 1, 1);


// =====================================================
// INFORMACIÓN FINAL
// =====================================================

print("");
print("==============================================");
print("HYPERSTACK TERMINADO");
print("==============================================");

print("Canales: " + nChannels);
print("Propiedades: " + nProps);
print("Focos: " + nZ);

print("");
print("CANALES:");

for (i = 0; i < nChannels; i++) {
    print("C" + (i+1) + " = " + channelList[i]);
}

print("");
print("PROPIEDADES:");

for (i = 0; i < nProps; i++) {
    print("Z" + (i+1) + " = " + propFiles[i]);
}

print("");
print("Imágenes encontradas: " + totalFound);
print("Planos vacíos o incompatibles: " + totalMissing);

print("Total de planos: " +
      (nChannels * nProps * nZ));

print("==============================================");
