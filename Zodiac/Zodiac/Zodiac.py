# Prompt the user for their sign
sign_input = input("Enter your astrological sign (e.g., Aries, Taurus, etc.): ").strip()

# Normalize input for comparison
sign = sign_input.lower()

if sign == "aries":
    print(r"""
   .-.   .-.
  (_  \ /  _)    Aries - The Ram
       |
       |
""")
elif sign == "taurus":
    print(r"""
    .     .
    '.___.'      Taurus - The Bull
    .'   `.
   :       :
   :       :
    `.___.'
""")
elif sign == "gemini":
    print(r"""
    ._____.
      | |        Gemini - The Twins
      | |
     _|_|_
    '     '
""")
elif sign == "cancer":
    print(r"""
      .--.
     /   _`.     Cancer - The Crab
    (_) ( )
   '.    /
     `--'
""")
elif sign == "leo":
    print(r"""
      .--.
     (    )       Leo - The Lion
    (_)  /
        (_,
""")
elif sign == "virgo":
    print(r"""
   _
  ' `:--.--.
     |  |  |_     Virgo - The Virgin
     |  |  | )
     |  |  |/
          (J
""")
elif sign == "libra":
    print(r"""
        __
   ___.'  '.___   Libra - The Balance
   ____________
""")
elif sign == "scorpio":
    print(r"""
   _
  ' `:--.--.
     |  |  |      Scorpius - The Scorpion
     |  |  |
     |  |  |  ..,
           `---':
""")
elif sign == "sagittarius":
    print(r"""
          ...
          .':     Sagittarius - The Archer
        .'
    `..'
    .'`.
""")
elif sign == "capricorn":
    print(r"""
            _
    \      /_)    Capricorn - The Goat
     \    /`.
      \  /   ;
       \/ __.'
""")
elif sign == "aquarius":
    print(r"""
 .-"-._.-"-._.-   Aquarius - The Water Bearer
 .-"-._.-"-._.-
""")
elif sign == "pisces":
    print(r"""
     `-.    .-'   Pisces - The Fishes
        :  :
      --:--:--
        :  :
     .-'    `-.
""")
else:
    print("Invalid sign. Please enter a valid astrological sign.")