const numbers = document.querySelectorAll("[data-number]");

if (numbers.length > 0) {
  const startNumberAnimation = (element) => {
    const number = +element.innerText;
    const numberDivision = number / 30;
    const animationRuntimeMS = 50;
    let dynamicNumber = 0;

    element.innerText = dynamicNumber;

    const animateNumbers = setInterval(() => {
      if (dynamicNumber < number) {
        dynamicNumber += numberDivision;
        element.innerText = Math.floor(dynamicNumber);
      } else {
        element.innerText = number;
        clearInterval(animateNumbers);
      }
    }, Math.random() * animationRuntimeMS);
  };

  numbers.forEach((number) => {
    startNumberAnimation(number);
  });
}