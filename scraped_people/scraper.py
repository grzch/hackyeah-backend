import json
import shutil

import requests
from bs4 import BeautifulSoup

data_filename = 'database.json'
polish_kings = ["Chościsko", "Piast the Wheelwright", "Siemowit", "Lestek", "Siemomysł", "Mieszko I",
                "Judith of Hungary", "Bolesław I Chrobry", "Emnilda of Lusatia", "Bezprym", "Mieszko II Lambert ",
                "Bolesław the Forgotten", "Casimir I the Restorer", "Bolesław II the Generous", "Przecława",
                "Władysław I Herman", "Judith of Bohemia", "Mieszko Bolesławowic", "Zbigniew", "Zbyslava of Kiev",
                "Bolesław III Wrymouth", "Salomea of Berg", "Władysław II the Exile", "Bolesław I the Tall",
                "Mieszko IV Tanglefoot", "Bolesław IV the Curly", "Mieszko III the Old", "Casimir II the Just",
                "Agnes of Poland", "Mstislav II of Kiev", "Odon of Poznań", "Henry I the Bearded", "Casimir I of Opole",
                "Władysław III Spindleshanks", "Konrad I of Masovia", "Leszek I the White", "Anastasia (Maria)",
                "Vsevolod IV of Kiev", "Roman the Great of Vladimir", "Władysław Odonic", "Henry II the Pious",
                "Bolesław V the Chaste", "Michael of Chernigov", "Maria of Halych", "Daniel of Galicia",
                "Bolesław the Pious", "Przemysł I of Greater Poland", "Elisabeth of Wrocław", "Bolesław II Rogatka",
                "Henry III the White", "Constance of Wrocław", "Casimir I of Kuyavia", "Euphrosyne of Opole",
                "Rostislav of Macsó ", "Leo I of Galicia", "Przemysł II", "Henryk IV Probus", "Leszek II the Black",
                "Ottokar II of Bohemia c.     ", "Kunigunda of Halych     ", "Rudolf I of Bohemia", "titular king",
                "Elisabeth Richeza of Poland", "Wenceslaus II of Bohemia", "Judith of Habsburg", "Hedwig of Kalisz   ",
                "Władysław I the Elbo w -high", "Yuri I of Galicia", "John of Bohemia", "titular king",
                "Elisabeth of Bohemia", "Wenceslaus III of Bohemia", "Anne of Bohemia", "Henry of Bohemia",
                "titular king", "Casimir III the Great", "Elisabeth of Poland", "Charles I of Hungary",
                "Anastasia of Halych", "William ", "Count of Celje", "Anna of Poland ", "Countess of Celje",
                "Louis I of Hungary", "Elisabeth of Poland", "Uliana of Tver", "Anna of Cilli", "Władysław II Jagiełło",
                "Jadwiga of Poland", "Elizabeth of Pomerania", "Sigismund ", "Holy Roman Emperor", "Sophia of Halshany",
                "Elizabeth of Luxembourg", "Władysław III", "Casimir IV", "Elizabeth of Austria",
                "Vladislaus II of Bohemia and Hungary", "John I Albert", "Alexander I", "Sigismund I the Old",
                "Anna of Poland", "Henry III", "Ferdinand I ", "Holy Roman Emperor", "Anne of Bohemia and Hungary",
                "Sophie of Pomerania", "Maximilian I", "Charles II ", "Archduke of Austria", "Elisabeth of Austria",
                "Sigismund II Augustus", "John III of Sweden", "Catherine Jagellon", "Anna Jagiellon",
                "Stephen Báthory", "Maximilian II", "Ferdinand II ", "Holy Roman Emperor", "Sigismund III Vasa",
                "John Adolf ", "Duke of Holstein-Gottorp", "Maria Anna of Austria", "Ferdinand III",
                "Holy Roman Emperor", "Cecilia Renata of Austria", "Władysław IV", "John II Casimir", "Frederick III ",
                "Duke of Holstei n -Gottorp", "John III Sobieski", "Ferdinand Maria ", "Elector of Bavaria",
                "Leopold I ", "Holy Roman Emperor", "Eleanor of Austria", "Michał Korybut Wiśniowiecki",
                "Christian Albert ", "Duke of Holstei n -Gottorp", "Theresa Kunegunda Sobieska",
                "Maximilian II Emanuel ", "Elector of Bavaria", "Maria Antonia of Austria", "Joseph I",
                "Holy Roman Emperor", "Augustus II the Strong", "Stanisław Leszczyński", "François Louis ",
                "Prince of Conti", "Christian August of Holstei n -Gottorp", "Prince of Eutin", "Frederick IV ",
                "Duke of Holstei n -GottorpMaria Josepha of Austria", "Augustus III", "Marie Leszczyńska",
                "Louis XV of France", "Joanna Elisabeth of Holstei n -Gottorp", "Charles Frederick ",
                "Duke of Holstei n -Gottorp", "Princess Maria Josepha of Saxony", "Louis ", "Dauphin of France",
                "Stanisław August Poniatowski", "Catherine the Great", "Peter III of Russia", "Paul I of Russia",
                "Alexander II", "Nicholas I", "Alexander III", "Alexander IV", "Nicholas II"]

pl_people = [
    "Roman Dmowski", "Frédéric Chopin", "Arthur Schopenhauer", "Marie Curie", "Catherine II of Russia",
    "Pope John Paul II",
    "Rosa Luxemburg", "Paul von Hindenburg", "Lech Wałęsa", "Heinz Guderian", "David Ben-Gurion",
    "Manfred von Richthofen", "Józef Piłsudski",
    "Isaac Bashevis Singer", "Johann Gottfried Herder", "Wernher von Braun", "Gabriel Fahrenheit", "Henryk Sienkiewicz",
    "Gerhart Hauptmann", "Max Born", "Erich Ludendorff", "Hans-Ulrich Rudel", "Günter Grass", "Billy Wilder",
    "Albert Abraham Michelson", "Krzysztof Kieślowski", "Arthur Rubinstein", "Fritz Haber", "Dietrich Bonhoeffer",
    "Edith Stein", "Paul Ehrlich", "Tadeusz Kościuszko", "Otto Stern", "Emil Adolf von Behring", "Werner von Blomberg",
    "Rudolf Virchow", "Kurt Lewin", "Ernst Cassirer", "Andrzej Wajda", "Konstantin Rokossovsky", "Janusz Korczak",
    "Maximilian Kolbe", "Władysław Szpilman", "Maria Leszczyńska", "Walther Nernst", "Leopold Kronecker",
    "Stefan Banach",
    "Erich von Falkenhayn", "Friedrich Daniel Ernst Schleiermacher", "Isidor Isaac Rabi", "Klaus Kinski",
    "Wojciech Jaruzelski", "Norbert Elias", "Günther von Kluge", "John II Casimir of Poland", "Horst Köhler",
    "Alfred Döblin", "Johannes Hevelius", "Ferdinand Lassalle", "Osip Mandelstam", "Irena Sendler", "Benoît Mandelbrot",
    "Carl Menger", "Alfred Tarski", "Wolfram von Richthofen", "Erwin von Witzleben", "Kurt Alder", "Edward Sapir",
    "Christian Wolff", "Krzysztof Penderecki", "Rudolf Clausius", "Antoni Grabowski", "Friedrich Bergius",
    "Henryk Wieniawski", "Władysław Reymont", "Anton Ivanovich Denikin", "Maria Göppert-Mayer", "Hanna Reitsch",
    "Georg Michaelis", "Dziga Vertov", "Elisabeth Schwarzkopf", "Reinhard Selten", "Jan Matejko", "Klaus von Klitzing",
    "Pola Negri", "Wisława Szymborska", "Adolph von Menzel", "Tadeus Reichstein", "Władysław Gomułka",
    "Faustyna Kowalska",
    "Otto Klemperer", "Siegbert Tarrasch", "Konrad Emil Bloch", "Egon Krenz", "Daniel Libeskind", "Witold Gombrowicz",
    "Zbigniew Brzezinski", "L. L. Zamenhof", "Ernst Kummer", "Paul Tillich", "Marian Rejewski", "Siegfried Lenz",
    "Stanisław Moniuszko", "Władysław Sikorski", "Kazimierz Kuratowski", "Gerhard Domagk", "Witold Lutosławski",
    "Albert Sabin", "Joseph Freiherr von Eichendorff", "Günter Blobel", "Bolesław Bierut", "Leonid Kravchuk",
    "Lech Kaczyński", "Karl Ludwig Hencke", "Felix Hausdorff", "Wacław Sierpiński", "Ignacy Łukasiewicz",
    "Vasily Sokolovsky", "Joseph Rotblat", "Miguel Najdorf", "Józef Gosławski", "Ignacy Mościcki", "Stanisław Konarski",
    "Hanna Schygulla", "Christa Wolf", "Andrzej W. Schally", "Donald Tusk", "Hagen Kleinert", "Aleksander Kwaśniewski",
    "Jarosław Kaczyński", "Leszek Kołakowski", "Henryk Górecki", "Bronisław Komorowski", "Sławomir Mrożek",
    "Grzegorz Lato", "Zbigniew Boniek", "Tadeusz Mazowiecki", "Bronisław Geremek", "Ryszard Kaczorowski",
]

people = ["Adolf Hitler", "Wolfgang Amadeus Mozart", "Napoleon Bonaparte", "Isaac Newton", "Albert Einstein",
          "Johann Sebastian Bach", "Ludwig van Beethoven", "Karl Marx", "Vincent van Gogh", "Immanuel Kant",
          "Sigmund Freud", "Pablo Picasso", "Johann Wolfgang von Goethe", "Voltaire", "Blaise Pascal", "Charles Darwin",
          "Che Guevara", "Jean-Jacques Rousseau", "Mahatma Gandhi", "Adam Smith", "Louis XIV of France",
          "Joseph Stalin", "Vladimir Lenin", "John Locke", "Martin Luther King, Jr.", "Friedrich Nietzsche",
          "Victor Hugo", "Elvis Presley", "Salvador Dalí", "Richard Wagner", "Molière", "Benito Mussolini",
          "Oscar Wilde", "Francisco Goya", "Claude Monet", "Frédéric Chopin", "Mao Zedong", "Marie Antoinette",
          "Carl Friedrich Gauss", "Giuseppe Verdi", "Otto von Bismarck", "Marilyn Monroe",
          "Georg Wilhelm Friedrich Hegel", "Louis Pasteur", "George Frideric Handel", "Carl Linnaeus",
          "Fyodor Dostoyevsky", "Max Weber", "Leo Tolstoy", "Gottfried Wilhelm von Leibniz", "Walt Disney",
          "Le Corbusier", "Jean-Paul Sartre", "Aleksandr Pushkin", "Winston Churchill", "Johannes Vermeer",
          "James Cook", "Benjamin Franklin", "Edgar Allan Poe", "Joseph Haydn", "Honoré de Balzac", "George Washington",
          "Thomas Edison", "Baruch Spinoza", "James Watt", "Anton Chekhov", "Abraham Lincoln", "Michael Faraday",
          "Jimi Hendrix", "Andy Warhol", "Antonio Vivaldi", "Mother Teresa", "Bob Marley", "Marcel Proust",
          "David Hume", "Bruce Lee", "Charles de Gaulle", "Peter I of Russia", "Bob Dylan", "Arthur Schopenhauer",
          "Francisco Franco", "Charlie Chaplin", "Hermann Hesse", "Friedrich Engels", "Rembrandt", "Paul Gauguin",
          "Heinrich Himmler", "Louis XVI of France", "Johannes Brahms", "John F. Kennedy", "George Orwell",
          "Mustafa Kemal Atatürk", "Thomas Mann", "Alfred Nobel", "Donatien Alphonse François de Sade, Marquis de Sade",
          "James Joyce", "Johann Christoph Friedrich von Schiller", "Fidel Castro", "Mark Twain", "Joseph Goebbels",
          "Marie Curie", "Bertolt Brecht", "Ernest Hemingway", "Charles Baudelaire", "Saddam Hussein",
          "Hans Christian Andersen", "John Maynard Keynes", "Antonín Dvořák", "Ludwig Wittgenstein", "Stanley Kubrick",
          "Jack the Ripper", "Nicholas II of Russia", "Frida Kahlo", "Gabriel García Márquez", "John Lennon",
          "Thomas Jefferson", "Daniel Defoe", "Hermann Göring", "Catherine II of Russia", "Napoleon III of France",
          "Pierre-Auguste Renoir", "Marlon Brando", "Pelé", "Pope John Paul II", "Basho", "Bertrand Russell",
          "Émile Zola", "Henry Ford", "Denis Diderot", "Charles de Secondat, baron de Montesquieu", "Giacomo Casanova",
          "Franklin D. Roosevelt", "Henri Matisse", "Henrik Ibsen", "Horatio Nelson, 1st Viscount Nelson",
          "Arthur Rimbaud", "Nikola Tesla", "Alessandro Volta", "Mikhail Gorbachev", "Édith Piaf",
          "Elizabeth II of the United Kingdom", "Max Planck", "William Blake", "Johnny Cash", "Ingmar Bergman",
          "Leon Trotsky", "Émile Durkheim", "Auguste Comte", "Michel Foucault", "Louis Armstrong", "Carl Jung",
          "Édouard Manet", "Stephen King", "Stendhal", "Giacomo Puccini", "Al Pacino", "Josip Broz Tito",
          "Marlene Dietrich", "Gustav Mahler", "Pablo Neruda", "Ronald Reagan", "Isaac Asimov", "Eugène Delacroix",
          "Franz Kafka", "Hirohito", "Erwin Rommel", "Hokusai", "Karl Popper", "Maximilien Robespierre",
          "Arthur Conan Doyle", "Woody Allen", "Alfred Hitchcock", "Frank Lloyd Wright", "Frank Sinatra",
          "Nikolai Gogol", "Rosa Luxemburg", "Audrey Hepburn", "Coco Chanel", "Robert Alexander Schumann",
          "Dmitri Mendeleev", "Pyotr Ilyich Tchaikovsky", "Franz Schubert", "Simón Bolívar", "Jean de La Fontaine",
          "Jean Piaget", "Clint Eastwood", "John Forbes Nash", "George Gordon Noel Byron, 6th Baron Byron",
          "Antoine Lavoisier", "Maria Theresa of Austria", "Anne Frank", "Paul McCartney", "Agatha Christie",
          "Maurice Ravel", "Niccolò Paganini", "Simone de Beauvoir", "Wilhelm II", "Franz Liszt", "Louis XV of France",
          "Nelson Mandela", "Wilhelm Conrad Röntgen", "John Dalton", "Nikita Khrushchev", "Luciano Pavarotti",
          "Al Capone", "Edgar Degas", "Stephen Hawking", "Richard Nixon", "Florence Nightingale", "Christiaan Huygens",
          "Giuseppe Garibaldi", "Edvard Grieg", "Mata Hari", "Robert De Niro", "Umberto Eco", "Samuel Beckett",
          "Jack Nicholson", "James Clerk Maxwell", "George Bernard Shaw", "Jack London", "Arnold Schwarzenegger",
          "Ernest Rutherford", "Louis XIII of France", "Jonathan Swift", "Alexander von Humboldt",
          "Alexander Graham Bell", "John Stuart Mill", "Hector Berlioz", "Jane Austen", "J. R. R. Tolkien",
          "Edvard Munch", "Jean Auguste Dominique Ingres", "Eric Clapton", "Roald Amundsen", "Alexander Fleming",
          "Charles Dickens", "Charles Perrault", "Enrico Fermi", "John von Neumann", "Heinrich Heine",
          "Astrid Lindgren", "Silvio Berlusconi", "Pol Pot", "Noam Chomsky", "Jacques-Louis David", "Leonid Brezhnev",
          "Jim Morrison", "Antoni Gaudí", "Felix Mendelssohn-Bartholdy", "Jules Verne", "Robert Koch",
          "Johann Pachelbel", "Robert Hooke", "Boris Yeltsin", "Ray Charles", "André-Marie Ampère", "Henri Bergson",
          "Chiang Kai-shek", "Richard Strauss", "Lewis Carroll", "Ferdinand de Saussure", "Chuck Norris",
          "Aleister Crowley", "Evangelista Torricelli", "Rudolf Steiner", "Josef Mengele", "George Harrison",
          "Harry S. Truman", "Maxim Gorky", "Virginia Woolf", "Bedřich Smetana", "George Sand", "Anders Celsius",
          "George Bush", "David Ricardo", "Brigitte Bardot", "Steven Spielberg", "Pope Benedict XVI", "Albert Camus",
          "Dwight D. Eisenhower", "Paul von Hindenburg", "Federico García Lorca", "Huang Xian Fan", "Rudyard Kipling",
          "Caspar David Friedrich", "Georges Bizet", "Adolf Eichmann", "Sun Yat-sen", "Lech Wałęsa",
          "Henri de Toulouse-Lautrec", "Theodore Roosevelt", "Georg Ohm", "Milan Kundera", "Freddie Mercury",
          "Ivan Pavlov", "J. M. W. Turner", "Gustave Eiffel", "James Prescott Joule", "Federico Fellini", "Ringo Starr",
          "Amedeo Modigliani", "Hayao Miyazaki", "Joan Miró", "Guglielmo Marconi", "Sylvester Stallone", "Ho Chi Minh",
          "Rainer Maria Rilke", "Grigori Rasputin", "Robert Boyle", "Anton Bruckner", "James Dean", "André Gide",
          "Sarah Bernhardt", "Augusto Pinochet", "Paul Verlaine", "Helen Keller", "Jean Sibelius", "Gustave Flaubert",
          "Albert Schweitzer", "Karl Dönitz", "Marcel Duchamp", "Gustave Courbet", "Sean Connery",
          "Pierre-Simon Laplace", "Warren Buffett", "Knut Hamsun", "Miles Davis", "Erich Fromm", "Tina Turner",
          "Jacques Offenbach", "Jimmy Carter", "Franz Joseph I of Austria", "John Milton", "Yasser Arafat",
          "Henry Dunant", "Walter Scott", "George H. W. Bush", "William Faulkner", "Eva Braun", "Wassily Kandinsky",
          "Béla Bartók", "H. P. Lovecraft", "Sophia Loren", "Antonio Salieri", "Octave Mirbeau", "Madame de Pompadour",
          "Jean Racine", "Kofi Annan", "Alvar Aalto", "Bill Gates", "Jean-Baptiste Lamarck", "Janis Joplin",
          "Antoine de Saint-Exupéry", "Ivan Turgenev", "Bernhard Riemann", "Charles Bukowski", "Georg Philipp Telemann",
          "Paul Klee", "Guy de Maupassant", "Erich Maria Remarque", "Louis XVIII of France",
          "Bernard Montgomery, 1st Viscount Montgomery of Alamein", "Malcolm X", "Anthony Hopkins", "Rudolf Hess",
          "Anatole France", "Piet Mondrian", "Frank Zappa", "Reinhard Heydrich", "John Wayne", "Mikhail Bakunin",
          "Emily Brontë", "Milton Friedman", "Woodrow Wilson", "Bill Clinton", "Abraham Maslow", "Jacques Chirac",
          "Edmund Husserl", "Joseph Conrad", "Rudolf Diesel", "Domenico Scarlatti", "Ennio Morricone", "Akihito",
          "Antonio Stradivari", "Yuri Andropov", "Wilhelm Keitel", "Søren Kierkegaard", "Sitting Bull",
          "Robert Baden-Powell, 1st Baron Baden-Powell", "Sergei Rachmaninoff", "Eva Perón", "Orson Welles",
          "Jean Cocteau", "Vladimir Vladimirovich Nabokov", "Jürgen Habermas", "Akira Kurosawa", "Pierre Curie",
          "Alexander I of Russia", "Stefan Zweig", "Dmitri Shostakovich", "Maurice Maeterlinck", "Leonhard Euler",
          "Leni Riefenstahl", "Guillaume Apollinaire", "John Dewey", "George Berkeley", "Camille Pissarro",
          "Paulo Coelho", "Theodor Mommsen", "Archduke Franz Ferdinand of Austria", "Erik Satie",
          "Alexander II of Russia", "James Brown", "Leonard Cohen", "Greta Garbo", "Chuck Berry", "John Steinbeck",
          "George Gershwin", "Henry Purcell", "Oskar Schindler", "Thomas Malthus", "Muhammad Ali",
          "Johann Gottlieb Fichte", "Dustin Hoffman", "Juan Carlos I of Spain", "Salvador Allende", "Harrison Ford",
          "Neil Armstrong", "Antoine Henri Becquerel", "Jimmy Page", "Jean-Baptiste Lully", "Camille Saint-Saëns",
          "Gustave Doré", "David Bowie", "Heinrich Böll", "Martin Bormann", "Ingrid Bergman",
          "Ludwig Andreas Feuerbach", "Novalis", "Carl Maria von Weber", "Romain Rolland", "David Hilbert",
          "Tomaso Albinoni", "Hu Jintao", "Pier Paolo Pasolini", "Charles Manson", "Modest Petrovich Mussorgsky",
          "Alain Delon", "Ozzy Osbourne", "Charles Babbage", "Joséphine de Beauharnais", "Konrad Adenauer",
          "Joseph Fourier", "Joseph Louis Lagrange", "Frederick II of Prussia", "Gregor Mendel", "Gaetano Donizetti",
          "Johann Heinrich Pestalozzi", "Walter Benjamin", "Christoph Willibald Gluck", "Elias Canetti",
          "Philip IV of Spain", "Herbert Spencer", "Vincenzo Bellini", "Francis Ford Coppola", "Jean-Paul Marat",
          "Idi Amin", "Ariel Sharon", "Yukio Mishima", "Emperor Meiji", "Jacques Lacan", "Nikolai Rimsky-Korsakov",
          "Henri Poincaré", "Karl Benz", "Carl Orff", "Mikhail Lermontov", "Vilfredo Pareto", "John D. Rockefeller",
          "Antonio Gramsci", "Paul Cézanne", "Albert Speer", "Pierre Corneille", "Aldous Huxley",
          "Anton van Leeuwenhoek", "Niels Henrik Abel", "Karl Jaspers", "Deng Xiaoping", "Georges Danton",
          "Nicholas I of Russia", "Catherine I of Russia", "Martin Scorsese", "André Breton", "Charles I of England",
          "Louis de Funès", "August Strindberg", "Jean-François Champollion", "Walt Whitman", "Humphrey Bogart",
          "Sully Prudhomme", "Yasunari Kawabata", "Roman Polański", "Évariste Galois", "Arcangelo Corelli",
          "Gerald Ford", "E.T.A. Hoffmann", "Abel Tasman", "Charles X of France", "Frédéric Mistral", "Hendrik Lorentz",
          "John III Sobieski", "Napoleon II of France", "Louis XVII of France", "Empress Dowager Cixi", "James Monroe",
          "Golda Meir", "Vangelis", "Truman Capote", "Bud Spencer", "Margaret Thatcher", "Indira Gandhi",
          "Wilhelm von Humboldt", "Konstantin Chernenko", "Philippe Pétain", "Carl von Clausewitz",
          "Joachim von Ribbentrop", "Muammar al-Gaddafi", "Empress Elisabeth of Austria",
          "Francis II, Holy Roman Emperor", "Alexander III of Russia", "Michelangelo Antonioni", "Jean-Philippe Rameau",
          "Boris Pasternak", "Charles-Augustin de Coulomb", "Christian Dior", "Queen Victoria", "David Lynch",
          "Jackie Chan", "Gustav Klimt", "Pierre Bourdieu", "Ernst Haeckel", "Arnold Schoenberg",
          "Anne of Great Britain", "Katharine Hepburn", "Daniel Bernoulli", "Henry David Thoreau", "Grace Kelly",
          "Ruhollah Khomeini", "Gioacchino Rossini", "Egon Schiele", "Friedrich Hölderlin", "T. S. Eliot", "Max Ernst",
          "Willy Brandt", "Douglas MacArthur", "Jacques Brel", "Kurt Gödel", "Gotthold Ephraim Lessing",
          "Edward Jenner", "Khalil Gibran", "Theodor W. Adorno", "Georges Braque", "William Herschel", "Lu Xun",
          "Heinz Guderian", "Erich von Manstein", "Pierre-Joseph Proudhon", "Charles Bronson", "Herbert von Karajan",
          "Gerd von Rundstedt", "Vladimir Putin", "Claude Debussy", "Louis Braille", "Roland Barthes",
          "Emiliano Zapata", "François-René de Chateaubriand", "David Livingstone", "Jacques Derrida",
          "Philip V of Spain", "Stéphane Mallarmé", "Prince Eugene of Savoy", "Carl Gustaf Emil Mannerheim",
          "António de Oliveira Salazar", "Eugène Ionesco", "David Ben-Gurion", "Paul I of Russia", "Pope Pius XII",
          "Giambattista Vico", "George VI of the United Kingdom", "Frank Gehry", "Nicolae Ceauşescu", "Lavrentiy Beria",
          "Helmut Kohl", "John Coltrane", "Leopold Mozart", "Amedeo Avogadro", "Michail Aleksandrovich Sholokhov",
          "Vasily Grigoryevich Zaitsev", "Vladimir Mayakovsky", "Gerhard Schröder", "Giorgio Armani", "Enzo Ferrari",
          "Mikhail Bulgakov", "Luis Buñuel", "Gavrilo Princip", "Fulgencio Batista", "Alexandre Dumas",
          "Richard Dawkins", "Henry Kissinger", "Carlo Goldoni", "Lyndon B. Johnson", "Georg Cantor", "Pope John XXIII",
          "Sergei Eisenstein", "Ralph Waldo Emerson", "William James", "Jean-Luc Godard", "Manfred von Richthofen",
          "Hannah Arendt", "Charles Aznavour", "Mohammad Reza Pahlavi", "Franz Beckenbauer", "Isaac Bashevis Singer",
          "Friedrich Wilhelm Joseph Schelling", "Antonio Canova", "Rabindranath Tagore", "Joseph John Thomson",
          "Charlotte Brontë", "Charles XII of Sweden", "Sergio Leone", "Mick Jagger", "Johann Gottfried Herder",
          "Farinelli", "Theodor Herzl", "Yuri Gagarin", "François Mitterrand", "Juan Perón",
          "Charles XIV John of Sweden", "Howard Hughes", "Fernando Pessoa", "Tenzin Gyatso, 14th Dalai Lama",
          "William-Adolphe Bouguereau", "Joachim Murat", "Roald Dahl", "Jean-François Millet", "Georges Simenon",
          "Charles II of Spain", "Fritz Lang", "Vivien Leigh", "Ivan Bunin", "Alfred Sisley", "Alfred Jodl",
          "Wernher von Braun", "Sergei Prokofiev", "Charlie Parker", "Erich Raeder", "Henry Cavendish", "John Adams",
          "Terence Hill", "Adam Mickiewicz", "Jean-Antoine Watteau", "Elton John", "Alexis de Tocqueville",
          "Heinrich Schliemann", "Georgy Zhukov", "Thomas Young", "James Madison", "Gamal Abdel Nasser", "Vitus Bering",
          "Charles II of England", "Alfred Adler", "Jean-Baptiste Colbert", "Luigi Galvani", "Buster Keaton", "Dalida",
          "Carl Philipp Emanuel Bach", "Charles Fourier", "Jack Kerouac", "Gabriel Fahrenheit",
          "Jules Cardinal Mazarin", "Gottlieb Daimler", "Edwin Hubble", "Henry James", "Slobodan Milošević",
          "Joseph II, Holy Roman Emperor", "Vyacheslav Molotov", "Franz von Papen", "Alexander Borodin",
          "Linus Pauling", "Robert Musil", "Jacob Bernoulli", "M. C. Escher", "Henry Miller", "Henry Fonda",
          "Henryk Sienkiewicz", "Judy Garland", "Gerhart Hauptmann", "Cyrano de Bergerac", "Maria Montessori",
          "Peter III of Russia", "Joseph Bonaparte", "Yoko Ono", "Jorge Luis Borges", "Michael Jackson", "Gregory Peck",
          "Carlos Santana", "William Wordsworth", "Peter Kropotkin", "Marcello Mastroianni",
          "William Thomson, 1st Baron Kelvin", "Mikhail Lomonosov", "Ulysses S. Grant", "Shimon Peres", "Edmund Burke",
          "Jean Reno", "Julio Iglesias", "Leonard Bernstein", "Fred Astaire", "Isabel Allende", "Paul Valéry",
          "Anwar Sadat", "Alexander Suvorov", "José Saramago", "William McKinley", "Emanuel Swedenborg",
          "Morgan Freeman", "Augustin Louis Cauchy", "Sukarno", "François Boucher", "Charles III of Spain", "Garrincha",
          "Catherine Deneuve", "Louis-Philippe I of France", "Robert Schuman", "Théodore Géricault", "Sting",
          "Dieterich Buxtehude", "Steve McQueen", "Joseph Louis Gay-Lussac", "Rudolf Christoph Eucken", "Sigrid Undset",
          "Ferenc Puskás", "Richard Feynman", "George Lucas", "Werner Heisenberg", "Klemens von Metternich",
          "William I", "Alessandro Scarlatti", "John Keats", "Marvin Gaye", "Charles VI, Holy Roman Emperor",
          "Johann Strauss II", "Percy Bysshe Shelley", "Ole Rømer", "Georges Pompidou", "Isadora Duncan",
          "Luigi Pirandello", "Jesse James", "Johan Cruijff", "Angela Merkel", "Robert Redford", "Max Born",
          "Alexander Pope", "Kim Il-sung", "Herbert Marcuse", "Ernst Kaltenbrunner", "Otto Skorzeny", "Anne Rice",
          "Carl Rogers", "William Butler Yeats", "Muhammad Yunus", "Kurt Waldheim", "Robert Owen", "Osamu Tezuka",
          "James II of England", "Frederick Winslow Taylor", "Michael Douglas", "Wilhelm Ostwald", "Pope Leo XIII",
          "Martin Buber", "Jacques-Yves Cousteau", "Marguerite Yourcenar", "Paul Dirac", "Joseph Schumpeter",
          "Imre Kertész", "Romy Schneider", "Enver Hoxha", "Johann Christian Bach", "George S. Patton", "Gabriel Fauré",
          "Ernst Röhm", "Haile Selassie I of Ethiopia", "Scatman John", "Haruki Murakami", "Pope Pius IX",
          "Honoré Daumier", "Lev Vygotsky", "Niels Henrik David Bohr", "Jackson Pollock", "Pieter Zeeman",
          "Michael Ende", "Kirk Douglas", "Man Ray", "B.B. King", "Elizabeth of Russia", "Kazimir Malevich",
          "Otto Hahn", "Max Stirner", "Cary Grant", "Andrew Jackson", "Clark Gable", "Hideki Tojo", "Charles Gounod",
          "Neil Young", "Pedro Almodóvar", "Billie Holiday", "Ernst Mach", "Alfred Tennyson, 1st Baron Tennyson",
          "Aleksandr Solzhenitsyn", "John Cage", "Bette Davis", "Bartolomé Estéban Murillo", "Anna Akhmatova",
          "Karl Ferdinand Braun", "Puyi", "Alfons Mucha", "Jean-Baptiste Camille Corot", "Django Reinhardt",
          "Ivo Andrić", "Erich Honecker", "Serge Gainsbourg", "Wolfgang Pauli", "Gottlob Frege", "Anthony Quinn",
          "Ferdinand Porsche", "Henri Rousseau", "Charles Maurice de Talleyrand-Périgord", "Konrad Lorenz",
          "Edward VIII of the United Kingdom", "Aram Khachaturian", "Justus von Liebig", "Pierre de Coubertin",
          "George Stephenson", "Gustav Kirchhoff", "Giovanni Battista Pergolesi", "Jeremy Bentham", "Alban Berg",
          "Erich Ludendorff", "Grover Cleveland", "Georges-Pierre Seurat", "Hans Frank", "George Boole",
          "Alfred Dreyfus", "Friedrich Paulus", "Barbra Streisand", "Paul Johann Ludwig von Heyse", "William Golding",
          "Jon Voight", "Gilles Deleuze", "Joseph Priestley", "Johannes Diderik van der Waals", "Ilya Yefimovich Repin",
          "John Bosco", "Anton LaVey", "Georg Simmel", "Mario Puzo", "Plácido Domingo", "Pope Pius XI",
          "Jiddu Krishnamurti", "Pope Paul VI", "Ástor Piazzolla", "Pedro Calderón de la Barca", "Hans-Ulrich Rudel",
          "Wilhelm Reich", "Alberto Moravia", "François Mauriac", "Al Gore",
          "Grand Duchess Anastasia Nikolaevna of Russia", "John Rawls", "Andrei Tarkovsky", "Jean Baudrillard",
          "Bhumibol Adulyadej", "Wilhelm Wundt", "William III of England", "Michael Caine", "Yitzhak Rabin",
          "Pope John Paul I", "George Best", "Syd Barrett", "Bjørnstjerne Bjørnson", "Marie Louise, Duchess of Parma",
          "Claus Schenk Graf von Stauffenberg", "Friedrich Hayek", "Rita Hayworth", "Naguib Mahfouz", "Gustave Moreau",
          "C. S. Lewis", "Alfred Wegener", "Raymond Chandler", "Carlos Slim Helú", "Victor Emmanuel III of Italy",
          "John Quincy Adams", "Erik Erikson", "José Martí", "Henry Morgan", "Ernst Werner von Siemens",
          "Keith Richards", "Louis Bonaparte", "Orhan Pamuk", "Kim Jong-il", "Olof Palme", "Sir Norman Foster",
          "Luchino Visconti", "Tristan Tzara", "Carlos Castaneda", "Georges Cuvier", "Marguerite Duras",
          "Philip K. Dick", "Auguste Rodin", "Isoroku Yamamoto", "Alfredo Di Stéfano", "René Magritte",
          "Toshiro Mifune", "Nadar", "Edward VII of the United Kingdom", "Ritchie Blackmore",
          "Luiz Inácio Lula da Silva", "Ezra Pound", "Giovanni Battista Tiepolo", "Nelly Sachs", "Christopher Lee",
          "Renzo Piano", "Bruce Springsteen", "Oriana Fallaci", "Francis Crick", "Lina Medina", "Geronimo",
          "Roger Waters", "Fridtjof Nansen", "Hermann von Helmholtz", "Lev Yashin", "Alphonse de Lamartine",
          "Meryl Streep", "Bruce Willis", "Pope Pius X", "Buffalo Bill", "Blackbeard", "Pope Pius VII",
          "Louis de Broglie", "Mikhail Glinka", "Carl Sagan", "Wilhelm Dilthey", "Octavio Paz", "Ed Gein",
          "Hans-Georg Gadamer", "Peter II of Russia", "François Couperin", "Mikhail Illarionovich Kutuzov",
          "Roger Martin du Gard", "Johnny Depp", "John Constable", "Ludwig Boltzmann", "Madame du Barry",
          "Mary Shelley", "Pearl S. Buck", "Ludwig Erhard", "Emperor Taishō", "Giovanni Domenico Cassini",
          "Oswald Spengler", "James D. Watson", "Denis Papin", "Christina, Queen of Sweden", "Viktor Frankl",
          "Victor Emmanuel II of Italy", "‘Abdu’l-Hamid II", "Augustus II the Strong", "Steven Seagal", "Peter Drucker",
          "Jacques Prévert", "Herbert Hoover", "Pancho Villa", "Günter Grass", "Kaspar Hauser", "Simo Häyhä",
          "Svante Arrhenius", "Robin Williams", "Dario Fo", "Gary Cooper", "César Franck", "Calvin Coolidge",
          "Rocky Marciano", "Elfriede Jelinek", "Edward Elgar", "George Soros", "Wilhelm Canaris", "Thomas Samuel Kuhn",
          "Jean le Rond d'Alembert", "Sergei Yesenin", "Ion Antonescu", "Joan Baez", "Andrei Sakharov", "Kurt Vonnegut",
          "Robert Oppenheimer", "Martin Van Buren", "Nina Simone", "Walter Model", "Billy Wilder",
          "Benjamin Disraeli, 1st Earl of Beaconsfield", "Fedor von Bock", "Wilhelm Frick", "Italo Calvino",
          "Paul Newman", "Isabella II of Spain", "Cecil John Rhodes", "Arthur Miller", "John Ruskin", "Zachary Taylor",
          "Marc-Antoine Charpentier", "Andrew Johnson", "Charles Lindbergh", "Alfred Russel Wallace",
          "Pio of Pietrelcina", "Giacomo Leopardi", "Franz Marc", "Maximilian I of Mexico", "David Gilmour",
          "Millard Fillmore", "Richard Sorge", "Simon Wiesenthal", "Tennessee Williams", "Alice Cooper", "Sid Vicious",
          "Albert Abraham Michelson", "Tove Jansson", "Marc Chagall", "Friedrich Ebert", "Stevie Wonder",
          "Leopold I, Holy Roman Emperor", "Claude Lévi-Strauss", "Humphry Davy", "Kangxi Emperor", "Anna of Russia",
          "Roger Moore", "Verner von Heidenstam", "Karel Čapek", "Dag Hammarskjöld", "Luigi Boccherini", "Phil Collins",
          "Grazia Deledda", "William Morris"]

famous_pl = ["Mikołaj Kopernik", "Jan Paweł II", "Józef Piłsudski", "Maria Skłodowska-Curie", "Lech Wałęsa",
             "Krystyna Skarbek", "Fryderyk Chopin", "Faustyna Kowalska", "Ignacy Łukasiewicz", "Ryszard Kukliński",
             "Joseph Conrad", "Stanisław Lem", "Jan Karski", "Jan III Sobieski", "Ignacy Domeyko", "Ernest Malinowski",
             "Ryszard Kapuściński", "Pola Negri", "Jan Kiepura", "Marian Rejewski, Jerzy Różycki, Henryk Zygalski",
             "Witold Pilecki", "Witold Gombrowicz", "Tadeusz Rozwadowski", "Czesław Miłosz", "Stefan Banach",
             "Bronisław Malinowski", "Władysław Anders", "Irena Sendler", "Witold Urbanowicz", "Władysław Jagiełło",
             "Tadeusz Kościuszko", "Janusz Korczak", "Helena Modrzejewska", "Zawisza Czarny", "Marek Edelman",
             "Zbigniew Brzeziński", "Henryk Mikołaj Górecki", "Wisława Szymborska", "Stanisław Sosabowski",
             "Zofia Rapp-Kochańska", "Paweł Włodkowic", "Józef Bem", "Kazimierz Leski", "Andrzej Wajda",
             "Leszek Kołakowski", "Stanisław Maczek", "Jan Heweliusz", "Kazimierz Pułaski", "Ludwik Zamenhof",
             "Józef Poniatowski", "Kazimierz Funk", "Helena Rubinstein", "Irena Szewińska", "Antoni Cierplikowski",
             "Jerzy Kukuczka", "Franciszek Żwirko", "Stanisław Wigura", "Jan Czochralski", "Jan Szczepanik",
             "Krzysztof Kieślowski", "Max Factor", "Władysław Reymont", "Stanisław Staszic", "Hugo Kołłątaj",
             "Stanisław Ulam", "Kazimierz Prószyński", "Henryk Sienkiewicz", "Benedykt Polak", "Krzysztof Komeda",
             "Rudolf Weigl", "Karol Szymanowski", "Jan Zamoyski", "Wanda Rutkiewicz", "Hilary Koprowski",
             "Władysław Szpilman", "Robert Lewandowski", " Jacek Odrowąż", "Bruno Schulz", "Ludwik Hirszfeld",
             "Roman Polański", "Xawery Dunikowski", "Tamara Łempicka", "Artur Rubinstein", "Zdzisław Starostecki",
             "Michał Czajkowski", "Zdzisław Beksiński", "Roman Opałka", "Janusz Kamiński", "Jerzy Kosiński",
             "Andrzej Czeczot", "Janusz Głowacki", "Urszula Dudziak", "Stefan Drzewicki", "Aleksander Józef Lisowski",
             "Michał Urbaniak", "Aleksander Wolszczan", "Rudolf Modrzejewski", "Mieczysław Bekker", "Andrzej Walicki",
             "Richard Pipes", "Jerzy Vetulani", "Krystian Zimerman"]


class Scrapy(object):
    def __init__(self, people):
        self.people = people
        self.scraped_people = []

    def start_scrapping(self, start_index=0):
        for person in self.people[start_index:]:
            self.scrap_person(person)

    def scrap_person(self, name):
        wiki_response = requests.get(self.get_wiki_url(name))
        soup = BeautifulSoup(wiki_response.content, 'html.parser')
        # img_url = soup.find("img", {"class": 'thumbimage'})

        article_id_start_index = wiki_response.text.index('wgArticleId":')
        if article_id_start_index == -1:
            print('img not found for ', name)
            return
        stripped_fragment = wiki_response.text[article_id_start_index + 13:article_id_start_index + 23]
        comma_index = stripped_fragment.index(',')
        article_id = stripped_fragment[:comma_index]
        img_url = 'http://pantheon.media.mit.edu/people/{}.jpg'.format(article_id)
        print(name, 'added!')
        local_img_url = self.download_image(name, img_url)
        if local_img_url is None:
            return
        self.scraped_people.append({
            'name': name,
            'img_url': img_url,
            'local_img_url': local_img_url,
            'wikipedia_paragraph': self.get_wikipedia(name, wiki_response)
        })
        self.save_json()

    def download_image(self, person_name, url):
        response = requests.get(url, stream=True)
        if response.status_code == 404:
            return None
        path = 'imgs/{}.jpg'.format(person_name)
        with open(path, 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
        del response
        return path

    @staticmethod
    def get_wiki_url(name):
        return 'https://en.wikipedia.org/wiki/{}'.format(name.replace(' ', '_'))

    def save_json(self):
        with open(data_filename) as f:
            saved_data = json.load(f)
            known_names = {person['name'] for person in saved_data}
        for new_person in self.scraped_people:
            if new_person["name"] in known_names:
                continue
            saved_data.append(new_person)
        with open(data_filename, 'w') as outfile:
            json.dump(saved_data, outfile, ensure_ascii=False)

    def get_wikipedia(self, name, wiki_response):
        soup = BeautifulSoup(wiki_response.content, 'html.parser')
        try:
            return soup.find_all('p')[1].text
        except (KeyError, IndexError):
            print('no wikipedia text for ', name)
            return ''


if __name__ == '__main__':
    scrap = Scrapy([
        'Emilia Plater'
    ])
    scrap.start_scrapping()
    scrap.save_json()
