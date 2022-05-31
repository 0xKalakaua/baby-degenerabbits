// SPDX-License-Identifier: MIT

/**

    (\ /)   (\ /)   (\ /)
    ( . .)  ( . .)  ( . .)
   C(")(")  C(")(") C(")(")

  Tombheads x FTM DEAD x 0xKalakaua - The Degenebabies - NFT Collection -

*/

pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/token/ERC721/IERC721.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721Enumerable.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/utils/Counters.sol";
import "@openzeppelin/contracts/access/AccessControl.sol";

contract Degenebabies is AccessControl, ERC721Enumerable, ERC721URIStorage {
    using Counters for Counters.Counter;
    using Strings for uint;

    Counters.Counter public tokenIdTracker;
    uint public immutable MAX_SUPPLY;

    mapping(uint => bool) private _rabbitHasBaby;
    mapping(uint => bool) private _lolasgirlHasBaby;
    string private _baseTokenURI;
    string private _baseExtension;
    string private _notRevealedURI;
    bool private _revealed = false;
    bool private _openMint;
    IERC721 private immutable _degenerabbits;
    IERC721 private immutable _lolasGirls;

    constructor (
        string memory name,
        string memory symbol, 
        string memory baseURI,
        string memory baseExtension,
        string memory notRevealedURI,
        uint max_supply,
        address rabbitsAddress,
        address lolasAddress,
        address admin
    )
        ERC721 (name, symbol)
    {
        tokenIdTracker.increment(); // Start collection at 1
        MAX_SUPPLY = max_supply;
        _baseTokenURI = baseURI;
        _baseExtension = baseExtension;
        _notRevealedURI = notRevealedURI;
        _openMint = false;
        _degenerabbits = IERC721(rabbitsAddress);
        _lolasGirls = IERC721(lolasAddress);
        _setupRole(DEFAULT_ADMIN_ROLE, admin);
        _setupRole(DEFAULT_ADMIN_ROLE, msg.sender);
    }

    modifier onlyAdmin() {
        require(hasRole(DEFAULT_ADMIN_ROLE, msg.sender), "caller is not admin");
        _;
    }

    function revealBabies() external onlyAdmin {
        _revealed = true;
    }

    function setBaseURI(string memory baseURI) external onlyAdmin {
        _baseTokenURI = baseURI;
    }

    function setBaseExtension(string memory baseExtension) external onlyAdmin {
        _baseExtension = baseExtension;
    }

    function setTokenURI(uint tokenId, string memory _tokenURI) external onlyAdmin {
        _setTokenURI(tokenId, _tokenURI);
    }

    function mintSwitch() external onlyAdmin {
        _openMint = !_openMint;
    }

    function makeBaby(uint rabbitTokenId, uint lolasTokenId) external {
        require(_openMint == true, "minting is currently not open");
        require(tokenIdTracker.current() <= MAX_SUPPLY, "all tokens have been minted");
        require(
            _rabbitHasBaby[rabbitTokenId] == false,
            "rabbit has a baby already"
        );
        require(
            _lolasgirlHasBaby[lolasTokenId] == false,
            "lolasGirl has a baby already"
        );
        require(
            _degenerabbits.ownerOf(rabbitTokenId) == msg.sender,
            "caller is not owner of that rabbit"
        );
        require(
            _lolasGirls.ownerOf(lolasTokenId) == msg.sender,
            "caller is not owner of that lolasGirl"
        );

        _rabbitHasBaby[rabbitTokenId] = true;
        _lolasgirlHasBaby[lolasTokenId] = true;

        _safeMint(msg.sender, tokenIdTracker.current());
        _setTokenURI(
            tokenIdTracker.current(),
            string(abi.encodePacked(tokenIdTracker.current().toString()))
        );
        tokenIdTracker.increment();

    }

    function makeBabyToWallet(address to, uint rabbitTokenId, uint lolasTokenId)
        external
        onlyAdmin
    {
        require(_openMint == true, "minting is currently not open");
        require(tokenIdTracker.current() <= MAX_SUPPLY, "all tokens have been minted");
        require(
            _rabbitHasBaby[rabbitTokenId] == false,
            "rabbit has a baby already"
        );
        require(
            _lolasgirlHasBaby[lolasTokenId] == false,
            "lolasGirl has a baby already"
        );
        require(
            _degenerabbits.ownerOf(rabbitTokenId) == to,
            "caller is not owner of that rabbit"
        );
        require(
            _lolasGirls.ownerOf(lolasTokenId) == to,
            "caller is not owner of that lolasGirl"
        );

        _rabbitHasBaby[rabbitTokenId] = true;
        _lolasgirlHasBaby[lolasTokenId] = true;

        _safeMint(to, tokenIdTracker.current());
        _setTokenURI(
            tokenIdTracker.current(),
            string(abi.encodePacked(tokenIdTracker.current().toString()))
        );
        tokenIdTracker.increment();

    }

    function rabbitHasBaby(uint rabbitTokenId) public view returns (bool) {
        return _rabbitHasBaby[rabbitTokenId];
    }

    function lolasGirlHasBaby(uint lolasTokenId) public view returns (bool) {
        return _lolasgirlHasBaby[lolasTokenId];
    }

    function tokenURI(uint tokenId)
        public
        view
        override(ERC721, ERC721URIStorage)
        returns (string memory)
    {
        if (!_revealed) {
            require(_exists(tokenId), "URI query for nonexistent token");
            return _notRevealedURI;
        }
        return string(abi.encodePacked(ERC721URIStorage.tokenURI(tokenId), _baseExtension));
    }

    function supportsInterface(bytes4 interfaceId)
        public
        view
        virtual override(AccessControl, ERC721, ERC721Enumerable)
        returns (bool)
    {
        return super.supportsInterface(interfaceId);
    }

    function _baseURI() internal view virtual override returns (string memory) {
        return _baseTokenURI;
    }

    function _burn(uint tokenId) internal virtual override(ERC721, ERC721URIStorage) {
        return ERC721URIStorage._burn(tokenId);
    }

    function _beforeTokenTransfer(address from, address to, uint tokenId)
        internal
        virtual override(ERC721, ERC721Enumerable)
    {
        super._beforeTokenTransfer(from, to, tokenId);
    }
}
