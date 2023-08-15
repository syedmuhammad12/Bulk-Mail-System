const inputs = document.querySelectorAll(".input-field");
const toggle_btn = document.querySelectorAll(".toggle");
const main = document.querySelector("main");
const bullets = document.querySelectorAll(".bullets span");
const images = document.querySelectorAll(".image");
// logo_image_upload
const imageContainer = document.getElementById("imageContainer");
const image = document.getElementById("preview");
const input = document.getElementById("fileInput");
const selectedFileName = document.getElementById("selectedFileName");

imageContainer.addEventListener("click", () => {
    input.click();
});

input.addEventListener("change", () => {
    if (input.files && input.files[0]) {
        const reader = new FileReader();

        reader.onload = (e) => {
            const img = new Image();
            img.src = e.target.result;

            img.onload = () => {
                const canvas = document.createElement("canvas");
                const ctx = canvas.getContext("2d");

                const maxSize = 150;
                let width = img.width;
                let height = img.height;

                if (width > height) {
                    if (width > maxSize) {
                        height *= maxSize / width;
                        width = maxSize;
                    }
                } else {
                    if (height > maxSize) {
                        width *= maxSize / height;
                        height = maxSize;
                    }
                }

                canvas.width = maxSize;
                canvas.height = maxSize;

                ctx.drawImage(img, (maxSize - width) / 2, (maxSize - height) / 2, width, height);

                image.src = canvas.toDataURL("image/jpeg");
            };
        };

        reader.readAsDataURL(input.files[0]);
    }
});

inputs.forEach((inp) => {
    inp.addEventListener("focus", () => {
        inp.classList.add("active");
    });
    inp.addEventListener("blur", () => {
        if (inp.value !== "") return;
        inp.classList.remove("active");
    });
});

toggle_btn.forEach((btn) => {
    btn.addEventListener("click", () => {
        main.classList.toggle("sign-up-mode");
    });
});

function moveSlider() {
    let index = this.dataset.value;

    let currentImage = document.querySelector(`.img-${index}`);
    images.forEach((img) => img.classList.remove("show"));
    currentImage.classList.add("show");

    const textSlider = document.querySelector(".text-group");
    textSlider.style.transform = `translateY(${-(index - 1) * 2.2}rem)`;

    bullets.forEach((bull) => bull.classList.remove("active"));
    this.classList.add("active");
}

bullets.forEach((bullet) => {
    bullet.addEventListener("click", moveSlider);
});

// Automatically move slider every 5 seconds
let currentSlide = 0;

function autoSlide() {
    currentSlide = (currentSlide + 1) % images.length;
    bullets[currentSlide].click();
}

setInterval(autoSlide, 1500);

// Additional code for file attachment
input.addEventListener("change", (event) => {
    const files = event.target.files;
    if (files.length > 0) {
        selectedFileName.textContent = files[0].name;
    } else {
        selectedFileName.textContent = "No file chosen";
    }
});
