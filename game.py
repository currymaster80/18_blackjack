from cards import Deck, hand_value


class Blackjack:
    def __init__(self):
        self.chips = 100

    def show(self, player, dealer, hide=True):
        shown_dealer = ["??"] if hide else [f"{r}{s}" for r, s in dealer]
        print("Dealer:", " ".join(shown_dealer))
        print("Player:", " ".join(f"{r}{s}" for r, s in player),
              "=", hand_value(player))

    def round(self):
        # Get a valid wager before starting the round
        while True:
            try:
                wager = int(input(f"Chips: {self.chips} | Wager: ").strip())
            except ValueError:
                print("Invalid wager.")
                continue

            if wager <= 0:
                print("Wager must be positive.")
            elif wager > self.chips:
                print("Wager cannot exceed your chips.")
            else:
                break

        deck = Deck()
        player = [deck.draw(), deck.draw()]
        dealer = [deck.draw(), deck.draw()]
        self.show(player, dealer)

        pv = hand_value(player)
        dv = hand_value(dealer)

        # Natural Blackjack
        if pv == 21:
            self.show(player, dealer, hide=False)

            if dv == 21:
                print("Push.")
            else:
                self.chips += wager
                print("Blackjack! Player wins.")

            return True

        # Player actions
        while hand_value(player) < 21:
            key = input("[h]it [s]tand [q]uit: ").strip().lower()

            if key == "q":
                print("Round cancelled.")
                return False

            if key == "s":
                print("Player stands.")
                break

            if key == "h":
                card = deck.draw()
                player.append(card)
                print("You drew:", f"{card[0]}{card[1]}")
                self.show(player, dealer)

                if hand_value(player) > 21:
                    self.chips -= wager
                    print("Bust. Dealer wins.")
                    print("Chips:", self.chips)
                    return True

            else:
                print("Invalid command. Use h, s, or q.")

        # Dealer draws until reaching 17
        while hand_value(dealer) < 17:
            card = deck.draw()
            dealer.append(card)
            print("Dealer draws:", f"{card[0]}{card[1]}")

        self.show(player, dealer, hide=False)

        pv, dv = hand_value(player), hand_value(dealer)

        # Settle the round exactly once
        if dv > 21:
            self.chips += wager
            print("Dealer busts. Player wins.")
        elif pv > dv:
            self.chips += wager
            print("Player wins.")
        elif pv < dv:
            self.chips -= wager
            print("Dealer wins.")
        else:
            print("Push.")

        print("Chips:", self.chips)
        return True

    def run(self):
        print("Blackjack — starting chips:", self.chips)

        while self.chips > 0:
            if not self.round():
                return

            if input("Play again? [y/n]: ").strip().lower() != "y":
                return