class byte:
	def __init__(self, value=0, bits=8):
		self.value = value % (2 ** bits)
		self.num = (2 ** bits)
		self.bits = bits
		
	def set(self, new_value):
		self.value = new_value % self.num
		
	def get(self):
		return self.value


class fc0011:
	def __init__(self):
		self.rr = byte(0, 1)
		self.sr = byte(0, 1)
		self.rro = byte(0, 1)
		self.ri = byte(0, 1)
		self.inp = byte(0, 1)
		self.out = byte(0, 1)
		self.acc = byte(0, 1)
		self.instr = byte(0x0, 4)
		self.fjmp = byte(0, 1)
		self.fskp = byte(0, 1)
	
	def reset(self):
		self.ri.set(0)
		self.acc.set(0)
		self.out.set(0)
	
	def exec(self, opcode, data):
		match opcode:
			case 0x0:
				pass
			case 0x1:
				self.rr.set(1)
				self.acc.set(self.inp.get())
			case 0x2:
				self.sr.set(1)
				self.out.set(self.acc.get())
			case 0x3:
				self.acc.set(self.acc.get() & self.inp.get())
			case 0x4:
				self.acc.set(self.acc.get() & ~ self.inp.get())
			case 0x5:
				self.acc.set(self.acc.get() | self.inp.get())
			case 0x6:
				self.acc.set(self.acc.get() | ~ self.inp.get())
			case 0x7:
				self.acc.set(self.acc.get() ^ self.inp.get())
			case 0x8:
				self.acc.set(self.acc.get() ^ ~ self.inp.get())
			case 0x9:
				self.acc.set(~ self.acc.get())
			case 0xA:
				self.rro.set(1)
				self.acc.set(self.inp.get())
			case 0xB:
				self.acc.set(self.inp.get())
			case 0xC:
				self.out.set(self.acc.get())
			case 0xD:
				self.fjmp.set(1)
			case 0xE:
				if ~ self.acc.get():
					self.fjmp.set(1)
			case 0xF:
				if ~ self.acc.get():
					self.fskp.set(1)
		
		if opcode != 0x1:
			self.rr.set(0)
		
		if opcode != 0x2:
			self.sr.set(0)
		
		if opcode != 0xA:
			self.rro.set(0)
		
		if (opcode != 0xD) | (opcode != 0xE):
			self.fjmp.set(0)
		
		if opcode != 0xF:
			self.fskp.set(0)

	def clock(self, data, inst):
		if self.ri:
			self.instr.set(inst)
			self.ri.set(0)
		else:
			self.exec(self.instr.get(), data)
			self.ri.set(1)
