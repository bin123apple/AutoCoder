// 定义 input_handler 模块
mod input_handler {
    pub struct InputHandler {}

    impl InputHandler {
        pub fn new() -> Self {
            Self {}
        }

        pub fn handle_input(&self) {
            println!("Handling general input...");
        }
    }
}

// 定义 keyboard 模块
mod keyboard {
    pub struct Keyboard {}

    impl Keyboard {
        pub fn new() -> Self {
            Self {}
        }

        pub fn handle_key_press(&self) {
            println!("Handling keyboard input...");
        }
    }
}

// 定义 mouse 模块
mod mouse {
    pub struct Mouse {}

    impl Mouse {
        pub fn new() -> Self {
            Self {}
        }

        pub fn handle_mouse_move(&self) {
            println!("Handling mouse movement...");
        }
    }
}

// 定义 gamepad 模块
mod gamepad {
    pub struct Gamepad {}

    impl Gamepad {
        pub fn new() -> Self {
            Self {}
        }

        pub fn handle_button_press(&self) {
            println!("Handling gamepad button press...");
        }
    }
}

// 定义 input 模块，将其他模块重新导出
mod input {
    pub use crate::input_handler::InputHandler;
    pub use crate::keyboard::Keyboard;
    pub use crate::mouse::Mouse;
    pub use crate::gamepad::Gamepad;
}

fn main() {
    // 实例化每个结构体
    let handler = input::InputHandler::new();
    let keyboard = input::Keyboard::new();
    let mouse = input::Mouse::new();
    let gamepad = input::Gamepad::new();

    // 调用每个实例的方法
    handler.handle_input();
    keyboard.handle_key_press();
    mouse.handle_mouse_move();
    gamepad.handle_button_press();

    println!("All inputs handled.");
}