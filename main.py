import SipRegistry

def main():
    print("Hello, world!")
    sipRegs = SipRegistry.SipRegistry("regs")
    print(sipRegs.getAorDataString('01574393bae33557c3000100620007'))

if __name__ == "__main__":
    main()
