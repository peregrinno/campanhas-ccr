const numbers = document.querySelectorAll("[data-number]");
const finalNumber = document.getElementById("fin-number");

if (numbers.length > 0) {
  const startNumberAnimation = (element, isFinal = false) => {
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
        if (isFinal) {
          const formattedNumber = number.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });
          element.innerText = formattedNumber;
        }
      }
    }, Math.random() * animationRuntimeMS);
  };

  numbers.forEach((number, index) => {
    startNumberAnimation(number, index === numbers.length - 1);
  });
}
